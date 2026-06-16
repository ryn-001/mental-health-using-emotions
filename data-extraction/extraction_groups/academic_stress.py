from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "exam stress",
    "study pressure",
    "academic stress",
    "failed exam",
    "low grades",
    "assignment deadline",
    "too much homework",
    "college stress",
    "university stress",
    "school stress",
    "can't focus on studies",
    "burnout from studying",
    "exam anxiety",
    "study anxiety",
    "competitive exams",
    "GPA pressure",
    "academic burnout",
    "late night studying",
    "student life is hard",
    "overwhelmed by studies"
]

def get_academic_stress_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "academic_stress", video["video_id"])
