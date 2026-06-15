from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "self improvement",
    "healing journey",
    "recovery",
    "therapy helped",
    "feeling better",
    "mental health recovery",
    "working on myself",
    "personal growth",
    "positive mindset",
    "gratitude",
    "motivated",
    "exercise helps",
    "meditation",
    "journaling",
    "small progress",
    "self care",
    "life is improving",
    "hope for the future",
    "healthy habits",
    "becoming stronger"
]

def get_positive_recovery_self_improvement_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "positive_recovery_self_improvement", video["video_id"])
