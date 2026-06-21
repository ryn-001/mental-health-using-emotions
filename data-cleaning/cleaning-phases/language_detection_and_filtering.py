import pandas as pd
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 42

def keep_english_text(text: str) -> bool:
    try:
        return detect(str(text)) == "en"
    except:
        return False
    
def filter_english_text(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    
    initial_count = len(df)
    df = df[df["comment_text"].apply(keep_english_text)].copy()
    final_count = len(df)

    video_id = path.split("/")[-1].split(".")[0]
    print(f"[Language Detection and Filtering] Removed comments {initial_count - final_count}")
    print(f"[Language Detection and Filtering] Remaining comments: {final_count}")
    print(f"[Language Detection and Filtering] Saved video {video_id} data", end="\n\n")

    return df
    