from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "cricket highlights",
    "football highlights",
    "tech reviews",
    "programming tutorials",
    "travel vlogs"
]

def get_neutral_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "neutral", video["video_id"])
