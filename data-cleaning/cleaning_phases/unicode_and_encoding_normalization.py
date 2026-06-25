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
    text = unicodedata.normalize("NFKC",text)

    # Remove invisible characters
    text = re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')

    return text

def unicode_and_encoding_normalization(df: pd.DataFrame) -> pd.DataFrame:
    
    initial_count = len(df)
    df["comment_text"] = df["comment_text"].apply(normalize_unicode)
    final_count = len(df)

    print(f"[Unicode and Encoding Normalization] Removed comments {initial_count - final_count}")
    print(f"[Unicode and Encoding Normalization] Remaining comments: {final_count}", end="\n\n")

    return df