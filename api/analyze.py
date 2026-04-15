from flask import Blueprint, request, jsonify
from services.youtube import YouTubeService
from services.sentiment import SentimentAnalyzer
from services.recommendation import get_recommendation
from config import YOUTUBE_API_KEY

analyze_bp = Blueprint("analyze", __name__)
_sa = SentimentAnalyzer()

def _get_youtube_service():
    return YouTubeService(YOUTUBE_API_KEY)


@analyze_bp.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)
    channel_id = data.get("channel_id", "").strip()
    video_count = max(1, min(int(data.get("video_count", 5)), 10))
    comments_per_video = max(1, min(int(data.get("comments_per_video", 20)), 100))

    if not channel_id:
        return jsonify({"error": "'channel_id' is required"}), 400

    try:
        youtube = _get_youtube_service()

        # 1. Channel info
        channel = youtube.get_channel_by_id(channel_id)
        if not channel:
            return jsonify({"error": "Channel not found"}), 404

        # 2. Latest videos
        videos = youtube.get_latest_videos(channel_id, max_results=video_count)
        if not videos:
            return jsonify({"error": "No public videos found for this channel"}), 404

        # 3. Per-video sentiment
        per_video = []
        all_comments: list[str] = []

        for video in videos:
            comments = youtube.get_comments(video["id"], max_results=comments_per_video)
            sentiments = _sa.analyze_comments(comments)
            per_video.append({
                "video": video,
                "comment_count": len(comments),
                "sentiments": sentiments,
            })
            all_comments.extend(comments)

        # 4. Aggregate
        aggregated = _sa.analyze_comments(all_comments)
        recommendation = get_recommendation(aggregated)

        return jsonify({
            "channel": channel,
            "videos_analyzed": len(videos),
            "total_comments": len(all_comments),
            "aggregated_sentiments": aggregated,
            "per_video_results": per_video,
            "recommendation": recommendation,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
