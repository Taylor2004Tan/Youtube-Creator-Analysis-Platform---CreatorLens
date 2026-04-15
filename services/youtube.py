from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeService:
    def __init__(self, api_key: str):
        self.api = build("youtube", "v3", developerKey=api_key)
        self._cache: dict = {}

    # ------------------------------------------------------------------ #
    #  Channel search (by keyword)
    # ------------------------------------------------------------------ #
    def search_channels(self, query: str, max_results: int = 5) -> list:
        try:
            resp = self.api.search().list(
                part="snippet",
                q=query,
                type="channel",
                maxResults=max_results,
            ).execute()
            results = []
            for item in resp.get("items", []):
                snip = item["snippet"]
                results.append({
                    "channel_id": item["id"]["channelId"],
                    "title": snip["title"],
                    "description": snip.get("description", "")[:150],
                    "thumbnail": snip["thumbnails"].get("medium", {}).get("url", ""),
                })
            return results
        except HttpError as e:
            raise RuntimeError(f"YouTube API error: {e}") from e

    # ------------------------------------------------------------------ #
    #  Resolve @handle → channel info
    # ------------------------------------------------------------------ #
    def get_channel_by_handle(self, handle: str) -> dict | None:
        key = f"handle:{handle}"
        if key in self._cache:
            return self._cache[key]
        try:
            resp = self.api.channels().list(
                part="snippet,statistics",
                forHandle=handle,
            ).execute()
            items = resp.get("items", [])
            if not items:
                return None
            result = self._format_channel(items[0])
            self._cache[key] = result
            return result
        except HttpError as e:
            raise RuntimeError(f"YouTube API error: {e}") from e

    # ------------------------------------------------------------------ #
    #  Get channel by ID
    # ------------------------------------------------------------------ #
    def get_channel_by_id(self, channel_id: str) -> dict | None:
        key = f"id:{channel_id}"
        if key in self._cache:
            return self._cache[key]
        try:
            resp = self.api.channels().list(
                part="snippet,statistics",
                id=channel_id,
            ).execute()
            items = resp.get("items", [])
            if not items:
                return None
            result = self._format_channel(items[0])
            self._cache[key] = result
            return result
        except HttpError as e:
            raise RuntimeError(f"YouTube API error: {e}") from e

    # ------------------------------------------------------------------ #
    #  Latest videos for a channel
    # ------------------------------------------------------------------ #
    def get_latest_videos(self, channel_id: str, max_results: int = 5) -> list:
        try:
            resp = self.api.search().list(
                part="snippet",
                channelId=channel_id,
                order="date",
                type="video",
                maxResults=max_results,
            ).execute()
            videos = []
            for item in resp.get("items", []):
                snip = item["snippet"]
                videos.append({
                    "id": item["id"]["videoId"],
                    "title": snip["title"],
                    "published_at": snip["publishedAt"],
                    "thumbnail": snip["thumbnails"].get("medium", {}).get("url", ""),
                })
            return videos
        except HttpError as e:
            raise RuntimeError(f"YouTube API error: {e}") from e

    # ------------------------------------------------------------------ #
    #  Comments for a video
    # ------------------------------------------------------------------ #
    def get_comments(self, video_id: str, max_results: int = 20) -> list:
        try:
            resp = self.api.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results, 100),
                textFormat="plainText",
                order="relevance",
            ).execute()
            comments = []
            for item in resp.get("items", []):
                text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(text)
            return comments
        except HttpError as e:
            # Comments disabled on this video
            if hasattr(e, "resp") and e.resp.status in (403, 400):
                return []
            raise RuntimeError(f"YouTube API error: {e}") from e
        except Exception:
            return []

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #
    def _format_channel(self, item: dict) -> dict:
        snip = item["snippet"]
        stats = item.get("statistics", {})
        return {
            "channel_id": item["id"],
            "title": snip["title"],
            "description": snip.get("description", "")[:200],
            "thumbnail": snip["thumbnails"].get("medium", {}).get("url", ""),
            "subscriber_count": stats.get("subscriberCount", "0"),
            "video_count": stats.get("videoCount", "0"),
        }
