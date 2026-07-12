from io import BytesIO
import os

import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceNotFoundError


def append_emotion_to_datalake(
    emotion_df: pd.DataFrame
) -> None:

    if emotion_df.empty:
        return

    load_dotenv()

    sas_token = os.getenv("SAS_TOKEN")

    if not sas_token:
        raise ValueError("SAS_TOKEN not found.")

    blob_url = (
        "https://ytcommentstorage.blob.core.windows.net/"
        "transformed-data/llm_cleaned.parquet"
    )

    blob_client = BlobClient.from_blob_url(
        blob_url=f"{blob_url}?{sas_token}"
    )

    try:

        download_stream = blob_client.download_blob()

        existing_df = pd.read_parquet(
            BytesIO(download_stream.readall()),
            engine="pyarrow"
        )

        combined_df = pd.concat(
            [existing_df, emotion_df],
            ignore_index=True
        )

    except ResourceNotFoundError:

        combined_df = emotion_df.copy()

    combined_df = combined_df.drop_duplicates(
        subset=["comment_id"]
    )

    parquet_buffer = BytesIO()

    combined_df.to_parquet(
        parquet_buffer,
        engine="pyarrow",
        index=False
    )

    parquet_buffer.seek(0)

    blob_client.upload_blob(
        parquet_buffer,
        overwrite=True
    )

    print(
        f"Saved {len(emotion_df)} new rows. "
        f"Total rows: {len(combined_df)}"
    )