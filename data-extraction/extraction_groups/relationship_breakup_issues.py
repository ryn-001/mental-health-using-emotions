from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "breakup recovery",
    "heartbreak story",
    "toxic relationship"
]

def get_relationship_breakup_issues_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "relationship_breakup_issues", video["video_id"])
