import re
import pandas as pd

SPAM_PATTERNS = [
    r"subscribe\s+to\s+my\s+channel",
    r"check\s+out\s+my\s+channel",
    r"check\s+out\s+my\s+video",
    r"follow\s+me",
    r"dm\s+me",
    r"whatsapp",
    r"telegram",
    r"earn\s+\$?\d+",
    r"crypto",
    r"bitcoin",
    r"investment",
    r"forex",
    r"click\s+here",
    r"visit\s+my\s+channel"
]

def is_spam(text: str) -> bool:
    if not isinstance(text, str):
        return True

    text = text.lower().strip()

    # Pattern-based spam
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text):
            return True

    # Phone numbers
    if re.search(r'\b\d{10,}\b', text):
        return True

    # Excessive repetition
    words = text.split()

    if len(words) >= 5:
        unique_ratio = len(set(words)) / len(words)

        if unique_ratio < 0.4:
            return True

    return False


def spam_bot_filtering(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)

    initial_count = len(df)

    df = df[~df["comment_text"].apply(is_spam)]

    final_count = len(df)

    video_id = path.split("/")[-1].split(".")[0]

    print(f"[Spam & Bot Filtering] Removed comments: {initial_count - final_count}")
    print(f"[Spam & Bot Filtering] Remaining comments: {final_count}")
    print(f"[Spam & Bot Filtering] Saved video {video_id} data", end="\n\n")

    return df