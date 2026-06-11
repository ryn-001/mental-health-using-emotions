from youtube_comment_downloader import YoutubeCommentDownloader

downloader = YoutubeCommentDownloader()

comments = downloader.get_comments_from_url(
    "https://www.youtube.com/watch?v=HSN7ISzmDfY"
)

for i, comment in enumerate(comments):
    print(comment["text"])
    if i == 99:
        break