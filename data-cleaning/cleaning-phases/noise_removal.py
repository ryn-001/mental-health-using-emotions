import re
import pandas as pd

def is_noise(text: str) -> bool:
    text = str(text).strip()

    if not text:
        return True

     # URL only
    if re.fullmatch(r'(https?://\S+|www\.\S+)', text):
        return True
    
    # Keep if at least one alphabetic character exists
    if any(char.isalpha() for char in text):
        return False

    return True

def noise_removal(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    initial_count = len(df)

    df = df[~df["comment_text"].apply(is_noise)]

    final_count = len(df)

    video_id = path.split("/")[-1].split(".")[0]

    print(f"[Noise Removal] Removed comments: {initial_count - final_count}")
    print(f"[Noise Removal] Remaining comments: {final_count}")
    print(f"[Noise Removal] Saved video {video_id} data", end="\n\n")

    return df