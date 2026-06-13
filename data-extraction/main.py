import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

print("Imported successfully")

load_dotenv()
youtube_comments_api_key = os.getenv("YOUTUBE_COMMENTS_API_KEY")

youtube = build("youtube","v3",developerKey=youtube_comments_api_key)

request = youtube.search().list(
    q="exam stress",
    part="snippet",
    type="video",
    maxResults=5
)

response = request.execute()

for i,item in enumerate(response['items']):
    print(f"\nVideo {i}")
    print("Title:", item["snippet"]["title"])
    print("Channel:", item["snippet"]["channelTitle"])
    print("Video ID:", item["id"]["videoId"])