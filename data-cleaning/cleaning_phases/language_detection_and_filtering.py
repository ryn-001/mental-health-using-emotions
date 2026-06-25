import pandas as pd
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 42

def keep_english_text(text: str) -> bool:
    try:
        return detect(str(text)) == "en"
    except:
        return False
    
def filter_english_text(df: pd.DataFrame) -> pd.DataFrame:
        
    initial_count = len(df)
    df = df[df["comment_text"].apply(keep_english_text)].copy()
    final_count = len(df)

    print(f"[Language Detection and Filtering] Removed comments {initial_count - final_count}")
    print(f"[Language Detection and Filtering] Remaining comments: {final_count}",end="\n\n")
    
    return df
    