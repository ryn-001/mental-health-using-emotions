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

def whitespace_normalization(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    
    initial_count = len(df)
    df["comment_text"] = df["comment_text"].apply(whitespace_check)
    final_count = len(df)

    video_id = path.split("/")[-1].split(".")[0]
    print(f"[Whitespace Normalization] Removed comments {initial_count - final_count}")
    print(f"[Whitespace Normalization] Remaining comments: {final_count}")
    print(f"[Whitespace Normalization] Saved video {video_id} data", end="\n\n")

    return df
