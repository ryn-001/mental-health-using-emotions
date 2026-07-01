from io import BytesIO
import os
import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobClient


def load_df_from_path(group_name: str, video_id: str) -> pd.DataFrame:

    load_dotenv()
    sas_token = os.getenv("SAS_TOKEN")

    if not sas_token:
        raise ValueError("SAS_TOKEN not found in environment variables")

    blob_url = (
        "https://ytcommentstorage.blob.core.windows.net/"
        f"raw-extracted-data/{group_name}/{video_id}.parquet"
    )

    blob_client = BlobClient.from_blob_url(
        blob_url=f"{blob_url}?{sas_token}"
    )

    download_stream = blob_client.download_blob()

    parquet_buffer = BytesIO(
        download_stream.readall()
    )

    df = pd.read_parquet(
        parquet_buffer,
        engine="pyarrow"
    )

    print(
        f"Loaded {len(df)} comments from "
        f"{group_name}/{video_id}.parquet"
    )

    return df