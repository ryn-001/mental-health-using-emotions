import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
SAS_TOKEN = os.getenv("SAS_TOKEN")


def read_parquet_from_blob(file_name):
    
    url = (
        f"https://ytcommentstorage.blob.core.windows.net/"
        f"cleaned-data/{file_name}.parquet?{SAS_TOKEN}"
    )

    return pd.read_parquet(url)