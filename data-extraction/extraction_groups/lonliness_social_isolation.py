from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "feeling alone",
    "loneliness",
    "social isolation",
    "no friends"
]

def get_loneliness_social_isolation_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "loneliness_social_isolation", video["video_id"])
