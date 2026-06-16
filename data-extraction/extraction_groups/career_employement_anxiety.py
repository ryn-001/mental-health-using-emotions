from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "can't find a job",
    "job anxiety",
    "career anxiety",
    "unemployed",
    "job rejection",
    "interview stress",
    "layoff",
    "lost my job",
    "career pressure",
    "career confusion",
    "work stress",
    "promotion anxiety",
    "salary stress",
    "toxic workplace",
    "job search",
    "job hunting",
    "fear of unemployment",
    "career uncertainty",
    "switching careers",
    "office stress"
]

def get_career_employment_anxiety_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "career_employment_anxiety", video["video_id"])
