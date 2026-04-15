from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self._vader = SentimentIntensityAnalyzer()

    def _classify(self, text: str) -> str:
        score = self._vader.polarity_scores(text)["compound"]
        if score >= 0.05:
            return "positive"
        if score <= -0.05:
            return "negative"
        return "neutral"

    def analyze_comments(self, comments: list) -> dict:
        if not comments:
            return {
                "positive": 0, "neutral": 0, "negative": 0,
                "total": 0,
                "positive_pct": 0.0, "neutral_pct": 0.0, "negative_pct": 0.0,
                "overall_score": 0.0,
            }

        counts = {"positive": 0, "neutral": 0, "negative": 0}
        total_compound = 0.0

        for comment in comments:
            label = self._classify(comment)
            counts[label] += 1
            total_compound += self._vader.polarity_scores(comment)["compound"]

        total = len(comments)
        return {
            "positive": counts["positive"],
            "neutral": counts["neutral"],
            "negative": counts["negative"],
            "total": total,
            "positive_pct": round(counts["positive"] / total * 100, 1),
            "neutral_pct": round(counts["neutral"] / total * 100, 1),
            "negative_pct": round(counts["negative"] / total * 100, 1),
            "overall_score": round(total_compound / total, 4),
        }
