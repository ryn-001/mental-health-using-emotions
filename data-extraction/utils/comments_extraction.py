import pandas as pd

def get_comments(youtube, video_id, maxComments = 100) -> pd.DataFrame:
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=maxComments,
        textFormat="plainText"
    )

    while request:
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']

            comments.append({
                'comment_id': item['snippet']['topLevelComent']['id'],
                'video_id': video_id,
                "author": comment.get("authorDisplayName"),
                "comment_text": comment.get("textDisplay"),
                "likes": comment.get("likeCount"),
                "published_at": comment.get("publishedAt")
            })

            if len(comments) >= maxComments:
                return pd.DataFrame(comments)
            
        request = youtube.commentThreads().list_next(request, response)

    return pd.DataFrame(comments)