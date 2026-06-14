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

            top_comment = item['snippet']['topLevelComment']
            snippet = top_comment['snippet']

            comments.append({
                'comment_id': top_comment['id'],
                'video_id': video_id,
                'author': snippet.get('authorDisplayName'),
                'comment_text': snippet.get('textDisplay'),
                'likes': snippet.get('likeCount'),
                'published_at': snippet.get('publishedAt')
            })
            
        request = youtube.commentThreads().list_next(request, response)

    return pd.DataFrame(comments)