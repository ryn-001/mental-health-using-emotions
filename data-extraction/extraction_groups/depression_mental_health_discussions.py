from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "depression",
    "feeling depressed",
    "mental health",
    "anxiety disorder",
    "panic attack",
    "therapy",
    "counseling",
    "I feel empty",
    "hopeless",
    "emotionally exhausted",
    "can't stop crying",
    "mental breakdown",
    "suicidal thoughts",
    "self harm",
    "lonely and depressed",
    "no motivation",
    "burnout",
    "mental illness",
    "crying every day",
    "need therapy"
]

def get_depression_mental_health_discussions_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "depression_mental_health_discussions", video["video_id"])
