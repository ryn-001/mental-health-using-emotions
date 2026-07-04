from io import BytesIO
import os

import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobClient


def read_parquet_from_blob(dataset_name: str) -> pd.DataFrame:

    load_dotenv()

    sas_token = os.getenv("SAS_TOKEN")

    if not sas_token:
        raise ValueError("SAS_TOKEN not found.")

    blob_url = (
        "https://ytcommentstorage.blob.core.windows.net/"
        f"transformed-data/{dataset_name}.parquet"
    )

    blob_client = BlobClient.from_blob_url(
        blob_url=f"{blob_url}?{sas_token}"
    )

    download_stream = blob_client.download_blob()

    parquet_bytes = BytesIO(download_stream.readall())

    df = pd.read_parquet(
        parquet_bytes,
        engine="pyarrow"
    )

    print(
        f"Loaded {len(df)} rows from {dataset_name}.parquet"
    )

    return df