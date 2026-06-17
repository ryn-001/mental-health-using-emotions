from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "overcoming anxiety",
    "therapy success",
    "mental health recovery",
    "self improvement"
]

def get_positive_recovery_self_improvement_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "positive_recovery_self_improvement", video["video_id"])
