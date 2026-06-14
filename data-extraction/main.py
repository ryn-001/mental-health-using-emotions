import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from extraction_groups.academic_stress import get_academic_stress_comments_by_videos

load_dotenv()
youtube_comments_api_key = os.getenv("YOUTUBE_COMMENTS_API_KEY")

youtube = build("youtube","v3",developerKey=youtube_comments_api_key)

get_academic_stress_comments_by_videos(youtube)