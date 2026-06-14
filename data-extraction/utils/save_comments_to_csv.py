import pandas as pd
from pathlib import Path

def save_comments(comments_df: pd.DataFrame, group_name: str, video_id: str):
    
    project_root = Path(__file__).parent.parent.parent

    save_dir = project_root / "data" / group_name
    save_dir.mkdir(parents=True, exist_ok=True)

    file_path = save_dir / f"{video_id}.csv"

    import pandas as pd
from pathlib import Path

def save_comments(comments_df: pd.DataFrame, group_name: str, video_id: str):
    
    project_root = Path(__file__).parent.parent.parent

    save_dir = project_root / "data" / group_name
    save_dir.mkdir(parents=True, exist_ok=True)

    file_path = save_dir / f"{video_id}.csv"

    comments_df.to_csv(
        file_path,
        mode="a",
        header=not file_path.exists(),
        index=False,
        encoding="utf-8"
    )

    print(f"Saved {len(comments_df)} comments to {file_path}")