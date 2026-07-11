"""
YouTube Comment Cleaning Pipeline
==================================
Flow: Azure Blob (raw .parquet) → LM Studio LLM → Azure Blob (cleaned .parquet)

Requirements:
    pip install azure-storage-blob pandas pyarrow requests tqdm

LM Studio Setup:
    - Load your model (recommended: Phi-3.5-mini-instruct Q4_K_M)
    - Enable the local server (default: http://localhost:1234)
    - Set context length to at least 512 tokens
"""

import io
import logging
import os
import time

import pandas as pd
import requests
from azure.storage.blob import ContainerClient
from tqdm import tqdm

# ─────────────────────────────────────────────
# CONFIGURATION — edit these before running
# ─────────────────────────────────────────────

SOURCE_CONTAINER_URL = os.environ["SOURCE_CONTAINER_URL"]
DEST_CONTAINER_URL = os.environ["DEST_CONTAINER_URL"]

COMMENT_COLUMN = "comment_text"  # column name holding the comment text
OUTPUT_COLUMNS = ["keep"]

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
LM_STUDIO_MODEL = "qwen2.5-1.5b-instruct"  # must match model name shown in LM Studio

# Processing knobs
BATCH_SIZE = 25  # comments sent per LLM call (tune based on speed)
MAX_WORKERS = 2  # parallel LLM requests (keep low on CPU inference)
REQUEST_TIMEOUT = 180  # seconds per LLM request
MAX_RETRIES = 3  # retries on LLM failure
RETRY_DELAY = 5  # seconds between retries

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("pipeline.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """You are a comment cleaning assistant. Your job is to clean YouTube comments.
For each comment, apply these rules:
1. Remove excessive punctuation (e.g., "!!!!!!" → "!")
2. Remove ALL CAPS shouting (convert to normal case)
3. Fix obvious spelling errors where confident
4. Remove spam patterns (repeated words, gibberish)
5. Remove emojis and special characters, keep only text
6. If a comment is pure spam/gibberish/offensive with no real content, replace it with [REMOVED]
7. Preserve the original language and meaning — do NOT translate
8. Keep it concise — do not add words not present in the original

Respond ONLY with the cleaned comment text, nothing else. No explanations, no labels."""


def build_user_prompt(comments: list[str]) -> str:
    lines = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(comments))
    return f"Comments:\n\n{lines}"


# ─────────────────────────────────────────────
# LM STUDIO CLIENT
# ─────────────────────────────────────────────


def call_lm_studio(comments: list[str]) -> list[dict]:
    """
    Send a batch of comments to LM Studio.
    Returns a list of annotation dicts, one per comment.
    """
    payload = {
        "model": LM_STUDIO_MODEL,
        "messages": [
            {"role": "user", "content": build_user_prompt(comments)},
        ],
        "temperature": 0.1,
        "max_tokens": min(len(comments) * 30, 1024),
        "stream": False,
    }

    fallback = [
        {
            "keep": None,
            "category": "unknown",
            "confidence": 0.0,
            "reason": "LLM call failed",
        }
        for _ in comments
    ]

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(LM_STUDIO_URL, json=payload, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            raw = resp.json()["choices"][0]["message"]["content"].strip()
            return parse_json_response(raw, len(comments))

        except requests.exceptions.Timeout:
            log.warning(f"Timeout (attempt {attempt}/{MAX_RETRIES})")
        except requests.exceptions.ConnectionError:
            log.error("Cannot reach LM Studio.")
            raise
        except Exception as e:
            log.warning(f"LLM error attempt {attempt}: {e}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)

    log.error(f"All {MAX_RETRIES} attempts failed — returning fallback for this batch.")
    return fallback


def parse_json_response(raw: str, expected_count: int) -> list[dict]:
    """Parse JSON array from LLM response."""
    import json

    # strip markdown fences if model adds them
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list) and len(parsed) == expected_count:
            return [
                {
                    "keep": item.get("keep"),
                    "category": item.get("category", "unknown"),
                    "confidence": item.get("confidence", 0.0),
                    "reason": item.get("reason", ""),
                }
                for item in parsed
            ]
        else:
            log.warning(
                f"Expected {expected_count} items, got {len(parsed)} — using fallback."
            )
    except json.JSONDecodeError as e:
        log.warning(f"JSON parse error: {e}")

    return [
        {
            "keep": None,
            "category": "unknown",
            "confidence": 0.0,
            "reason": "parse failed",
        }
        for _ in range(expected_count)
    ]


def annotate_dataframe(df: pd.DataFrame, local_save_path: str = None) -> pd.DataFrame:
    if COMMENT_COLUMN not in df.columns:
        raise ValueError(
            f"Column '{COMMENT_COLUMN}' not found. Available: {list(df.columns)}"
        )

    comments = df[COMMENT_COLUMN].fillna("").tolist()
    all_annotations = []

    batches = [
        comments[i : i + BATCH_SIZE] for i in range(0, len(comments), BATCH_SIZE)
    ]
    log.info(
        f"Annotating {len(comments):,} comments in {len(batches)} batches (size={BATCH_SIZE})"
    )

    with tqdm(total=len(comments), desc="Annotating", unit="comment") as pbar:
        offset = 0
        for batch in batches:
            result = call_lm_studio(batch)
            all_annotations.extend(result)

            if local_save_path:
                batch_df = df.iloc[offset : offset + len(batch)].copy()
                for col in OUTPUT_COLUMNS:
                    batch_df[col] = [r[col] for r in result]
                save_batch_locally(batch_df, local_save_path)

            offset += len(batch)
            pbar.update(len(batch))

    df = df.copy()
    for col in OUTPUT_COLUMNS:
        df[col] = [a[col] for a in all_annotations]

    return df


# ─────────────────────────────────────────────
# AZURE HELPERS
# ─────────────────────────────────────────────


def get_container_clients():
    source = ContainerClient.from_container_url(SOURCE_CONTAINER_URL)
    dest = ContainerClient.from_container_url(DEST_CONTAINER_URL)
    return source, dest


def list_parquet_blobs(container_client) -> list[str]:
    blobs = [
        b.name for b in container_client.list_blobs() if b.name.endswith(".parquet")
    ]
    log.info(f"Found {len(blobs)} .parquet files")
    return blobs


def download_parquet(container_client, blob_name: str) -> pd.DataFrame:
    data = container_client.get_blob_client(blob_name).download_blob().readall()
    return pd.read_parquet(io.BytesIO(data))


def upload_parquet(container_client, blob_name: str, df: pd.DataFrame):
    buf = io.BytesIO()
    df.to_parquet(buf, index=False, engine="pyarrow")
    buf.seek(0)
    container_client.get_blob_client(blob_name).upload_blob(buf, overwrite=True)


def already_processed(container_client, blob_name: str) -> bool:
    try:
        container_client.get_blob_client(blob_name).get_blob_properties()
        return True
    except Exception:
        return False


# ─────────────────────────────────────────────
# LOCAL STORAGE
# ─────────────────────────────────────────────


def save_batch_locally(batch_df: pd.DataFrame, local_path: str):
    """Append a batch to a local parquet file incrementally."""
    if os.path.exists(local_path):
        existing = pd.read_parquet(local_path)
        combined = pd.concat([existing, batch_df], ignore_index=True)
    else:
        combined = batch_df
    combined.to_parquet(local_path, index=False, engine="pyarrow")


# ─────────────────────────────────────────────
# CORE PROCESSING
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────


def run_pipeline(parallel: bool = False):
    log.info("=" * 60)
    log.info("YouTube Comment Cleaning Pipeline — Starting")
    log.info("=" * 60)

    # Verify LM Studio is reachable before doing any Azure work
    try:
        test = requests.get("http://localhost:1234/v1/models", timeout=5)
        test.raise_for_status()
        log.info(
            f"LM Studio reachable. Models: {[m['id'] for m in test.json().get('data', [])]}"
        )
    except Exception as e:
        log.error(f"LM Studio not reachable: {e}")
        log.error("Start LM Studio, load a model, and enable the local server first.")
        return

    source_client, dest_client = get_container_clients()  # ← only this line changed

    blobs = list_parquet_blobs(source_client)  # ← and these now take a client directly
    if not blobs:
        log.warning("No .parquet files found in source container.")
        return

    success, skipped, failed = 0, 0, 0

    for blob_name in blobs:
        log.info(f"\n── Processing: {blob_name}")

        if already_processed(
            dest_client, blob_name
        ):  # ← dest_client instead of (client, container, blob)
            log.info(f"  Already in destination — skipping.")  # noqa: F541
            skipped += 1
            continue

        try:
            df = download_parquet(source_client, blob_name)

            local_path = f"local_annotated/{blob_name}"
            os.makedirs("local_annotated", exist_ok=True)
            df_annotated = annotate_dataframe(df, local_save_path=local_path)

            upload_parquet(dest_client, blob_name, df_annotated)
            success += 1

        except Exception as e:
            log.error(f"  FAILED for '{blob_name}': {e}", exc_info=True)
            failed += 1

    log.info("\n" + "=" * 60)
    log.info(
        f"Pipeline complete — Success: {success} | Skipped: {skipped} | Failed: {failed}"
    )
    log.info("=" * 60)


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Set parallel=True only if you have sufficient RAM and the model is loaded once
    run_pipeline(parallel=False)
