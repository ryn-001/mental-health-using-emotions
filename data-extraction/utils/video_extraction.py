import re


def contains_many_non_english_chars(
    title: str,
    threshold: int = 10
) -> bool:

    non_ascii = re.findall(
        r'[^\x00-\x7F]',
        title
    )

    return len(non_ascii) > threshold


def get_comment_count(
    youtube,
    video_id
) -> int:

    response = youtube.videos().list(
        part="statistics",
        id=video_id
    ).execute()

    if not response["items"]:
        return 0

    statistics = response["items"][0]["statistics"]

    return int(
        statistics.get(
            "commentCount",
            0
        )
    )


def get_videos(
    youtube,
    queries,
    videos_per_query=5,
    min_comments=500,
    max_comments=1000
):

    videos = []

    for query in queries:

        print(f"\nSearching query: {query}")

        query_videos = 0
        next_page_token = None

        while query_videos < videos_per_query:

            response = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                relevanceLanguage="en",
                videoDuration="medium",
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            items = response.get(
                "items",
                []
            )

            if not items:
                break

            for item in items:

                video_id = item["id"]["videoId"]

                title = item["snippet"]["title"]

                if contains_many_non_english_chars(
                    title
                ):
                    continue

                try:

                    comment_count = get_comment_count(
                        youtube,
                        video_id
                    )

                except Exception as e:

                    print(
                        f"Failed: {video_id}"
                    )

                    continue

                if (
                    comment_count < min_comments
                    or
                    comment_count > max_comments
                ):
                    continue

                videos.append({

                    "video_id":
                        video_id,

                    "title":
                        title,

                    "channel":
                        item["snippet"][
                            "channelTitle"
                        ],

                    "query":
                        query,

                    "comment_count":
                        comment_count

                })

                query_videos += 1

                print(
                    f"✓ [{query_videos}/{videos_per_query}] "
                    f"{title} "
                    f"({comment_count} comments)"
                )

                if (
                    query_videos
                    >= videos_per_query
                ):
                    break

            next_page_token = response.get(
                "nextPageToken"
            )

            if not next_page_token:
                break

        print(
            f"Collected "
            f"{query_videos} videos "
            f"for '{query}'"
        )

    return videos