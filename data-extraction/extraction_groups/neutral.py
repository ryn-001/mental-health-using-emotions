from utils.video_extraction import get_videos
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

QUERIES = [
    "today was normal",
    "weather is nice",
    "good morning",
    "what are you doing",
    "random thoughts",
    "daily routine",
    "ate lunch",
    "going to work",
    "watching TV",
    "reading a book",
    "walking outside",
    "cooking dinner",
    "shopping today",
    "weekend plans",
    "traffic today",
    "learning python",
    "new movie",
    "travel plans",
    "news update",
    "general discussion"
]

def get_neutral_comments_by_videos(youtube):

    videos = get_videos(youtube, QUERIES)

    for video in videos:
        comments_df = get_comments(youtube, video["video_id"])
        save_comments(comments_df, "neutral", video["video_id"])
