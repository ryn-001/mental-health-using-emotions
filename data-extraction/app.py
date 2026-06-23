from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
from flask_cors import CORS
from utils.comments_extraction import get_comments
from utils.save_comments_to_csv import save_comments

load_dotenv()

youtube_comments_api_key = os.getenv(
    "YOUTUBE_COMMENTS_API_KEY"
)

youtube = build(
    "youtube",
    "v3",
    developerKey=youtube_comments_api_key
)

app = Flask(__name__)
CORS(app)

@app.route(
    "/extract-comments",
    methods=["POST"]
)
def extract_comments():

    try:

        data = request.get_json()

        video_id = data.get("video_id")
        group_name = data.get("group_name")

        if not video_id:
            return jsonify({
                "success": False,
                "message": "video_id is required"
            }), 400

        if not group_name:
            return jsonify({
                "success": False,
                "message": "group_name is required"
            }), 400

        comments_df = get_comments(
            youtube,
            video_id
        )

        if comments_df.empty:
            return jsonify({
                "success": False,
                "message": "No comments found"
            }), 404

        save_comments(
            comments_df,
            group_name,
            video_id
        )

        return jsonify({
            "success": True,
            "video_id": video_id,
            "group_name": group_name,
            "comments_extracted": len(comments_df)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )