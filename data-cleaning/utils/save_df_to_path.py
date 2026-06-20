from io import BytesIO
import os
import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobClient


def save_df_to_path(comments_df: pd.DataFrame, group_name: str, video_id: str):

    load_dotenv()
    sas_token = os.getenv("SAS_TOKEN")

    if not sas_token:
        raise ValueError("SAS_TOKEN not found in environment variables")

    blob_url = (
        "https://ytcommentstorage.blob.core.windows.net/"
        f"cleaned-data/{group_name}/{video_id}.parquet"
    )

    blob_client = BlobClient.from_blob_url(
        blob_url=f"{blob_url}?{sas_token}"
    )

    parquet_buffer = BytesIO()

    comments_df.to_parquet(
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
        f"Saved {len(comments_df)} comments to "
        f"{group_name}/{video_id}.parquet"
    )