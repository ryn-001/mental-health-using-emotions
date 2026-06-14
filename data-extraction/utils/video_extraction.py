MIN_COMMENTS = 500

def get_comment_count(youtube, video_id):

    response = youtube.videos().list(
        part="statistics",
        id=video_id
    ).execute()

    if not response["items"]:
        return 0

    statistics = response["items"][0]["statistics"]

    return int(statistics.get("commentCount", 0))

def get_videos(youtube, queries) -> list:

    videos = []

    for query in queries:

        response = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=20
        ).execute()

        for item in response["items"]:

            video_id = item["id"]["videoId"]

            comment_count = get_comment_count(
                youtube,
                video_id
            )

            if comment_count < MIN_COMMENTS:
                continue

            videos.append({
                "video_id": video_id,
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "query": query,
                "comment_count": comment_count
            })

    return videos