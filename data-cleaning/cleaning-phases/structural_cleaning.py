import pandas as pd
from utils.save_df_to_path import save_df_to_path

def structural_cleaning(path):
    df = pd.read_parquet(path)
    initial_count = len(df)

    # 1. Removing NULL comments
    df = df[df["comment_text"].notna()]

    # 2. Removing Empty comments
    df = df[df["comment_text"] != ""]

    # 3. Removing Whitespace-only comments
    df = df[df["comment_text"].str.strip() != ""]

    # 4. Removing Duplicates
    df = df.drop_duplicates(subset=["comment_text"])

    # 5. Remving Deleted or Unavailable comments
    INVALID_TEXTS = [
        "[deleted]",
        "[removed]",
        "deleted",
        "removed"
    ]
    df = df[~df["comment_text"].isin(INVALID_TEXTS)]

    final_count = len(df)
    video_id = path.split("/")[-1].split(".")[0]

    print(f"[Structural Cleaning] Removed comments {initial_count - final_count}")
    print(f"[Structural Cleaning] Remaining comments: {final_count}")
    save_df_to_path(df,path, video_id)
    print(f"[Structural Cleaning] Saved video {video_id} data")


