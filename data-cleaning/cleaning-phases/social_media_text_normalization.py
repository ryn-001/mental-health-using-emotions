import re
import pandas as pd

CONTRACTIONS = {
    "i'm": "i am",
    "can't": "cannot",
    "won't": "will not",
    "don't": "do not",
    "didn't": "did not",
    "isn't": "is not",
    "aren't": "are not",
    "i've": "i have",
    "i'll": "i will",
    "it's": "it is"
}

def normalize_social_text(text: str) -> str:
    if not isinstance(text, str):
        return text

    # Replace URLs
    text = re.sub(r'https?://\S+|www\.\S+', '<URL>', text)

    # Replace user mentions
    text = re.sub(r'@\w+', '<USER>', text)

    # Expand contractions
    for contraction, expanded in CONTRACTIONS.items():
        text = re.sub(
            rf'\b{re.escape(contraction)}\b',
            expanded,
            text,
            flags=re.IGNORECASE
        )

    # Normalize repeated characters
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    return text

def social_media_text_normalization(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    initial_count = len(df)

    df["comment_text"] = (
        df["comment_text"]
        .apply(normalize_social_text)
    )

    final_count = len(df)

    video_id = path.split("/")[-1].split(".")[0]
    print(f"[Unicode and Encoding Normalization] Removed comments {initial_count - final_count}")
    print(f"[Unicode and Encoding Normalization] Remaining comments: {final_count}")
    print(f"[Unicode and Encoding Normalization] Saved video {video_id} data", end="\n\n")

    return df