import re
import ftfy
import unicodedata
import pandas as pd

def normalize_unicode(text: str) -> str:

    if not isinstance(text,str):
        return text

    # Fix encoding issues
    text = ftfy.fix_text(text)

    # Unicode Normalization
    text = unicodedata.normalize("NKFC",text)

    # Remove invisible characters
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')

    return text

def unicode_and_encoding_normalization(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    
    initial_count = len(df)
    df["comment_text"] = df["comment_text"].apply(normalize_unicode)
    final_count = len(df)

    video_id = path.split("/")[-1].split(".")[0]
    print(f"[Unicode and Encoding Normalization] Removed comments {initial_count - final_count}")
    print(f"[Unicode and Encoding Normalization] Remaining comments: {final_count}")
    print(f"[Unicode and Encoding Normalization] Saved video {video_id} data", end="\n\n")

    return df