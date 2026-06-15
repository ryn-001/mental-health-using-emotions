from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "financial stress",
    "money problems",
    "can't pay bills",
    "debt",
    "loan repayment",
    "credit card debt",
    "living paycheck to paycheck",
    "rent is too high",
    "inflation",
    "can't afford",
    "financial anxiety",
    "bankruptcy",
    "lost savings",
    "salary not enough",
    "poor financial situation",
    "cost of living",
    "student loan",
    "medical bills",
    "struggling financially",
    "no money"
]

def get_financial_stress_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "financial_stress", video["video_id"])
