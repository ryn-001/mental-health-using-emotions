import re
import pandas as pd

def whitespace_check(text: str) -> str:
    if not isinstance(text, str):
        return text

    # Replace all whitespaces with single space
    text = re.sub(r'\s+',' ',text)

    # Remove leading and trailing whitespaces
    text = text.strip()

    return text

def whitespace_normalization(df: pd.DataFrame) -> pd.DataFrame:
    
    initial_count = len(df)
    df["comment_text"] = df["comment_text"].apply(whitespace_check)
    final_count = len(df)

    print(f"[Whitespace Normalization] Removed comments {initial_count - final_count}")
    print(f"[Whitespace Normalization] Remaining comments: {final_count}",end="\n\n")

    return df
