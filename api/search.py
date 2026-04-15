from flask import Blueprint, request, jsonify
from services.youtube import YouTubeService
from config import YOUTUBE_API_KEY

search_bp = Blueprint("search", __name__)

def _get_youtube_service():
    return YouTubeService(YOUTUBE_API_KEY)


@search_bp.route("/api/search")
def search_channels():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    try:
        results = _get_youtube_service().search_channels(query, max_results=6)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
