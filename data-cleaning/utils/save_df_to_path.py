from io import BytesIO
import os
import pandas as pd
from dotenv import load_dotenv
from azure.storage.blob import BlobClient
from azure.core.exceptions import ResourceNotFoundError


def append_df_to_path(
    new_df: pd.DataFrame,
    group_name: str
) -> None:

    if new_df.empty:
        print(
            f"[Append] Skipped {group_name}. "
            "DataFrame is empty."
        )
        return

    load_dotenv()
    sas_token = os.getenv("SAS_TOKEN")

    if not sas_token:
        raise ValueError(
            "SAS_TOKEN not found in environment variables"
        )

    blob_url = (
        "https://ytcommentstorage.blob.core.windows.net/"
        f"cleaned-data/{group_name}.parquet"
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
            [existing_df, new_df],
            ignore_index=True
        )

        print(
            f"[Append] Loaded "
            f"{len(existing_df)} existing comments."
        )

    except ResourceNotFoundError:
        combined_df = new_df.copy()

        print(
            f"[Append] {group_name}.parquet not found. "
            "Creating new file."
        )

    before = len(combined_df)

    combined_df = combined_df.drop_duplicates()

    removed = before - len(combined_df)

    if removed > 0:
        print(
            f"[Append] Removed "
            f"{removed} duplicate rows."
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
        f"[Append] Saved "
        f"{len(combined_df)} comments to "
        f"{group_name}.parquet"
    )