from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "exam stress",
    "study burnout",
    "failed exam motivation",
    "student mental health"
]

def get_academic_stress_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "academic_stress", video["video_id"])
