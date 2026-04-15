def get_recommendation(sentiment_data: dict) -> dict:
    pos_pct = sentiment_data.get("positive_pct", 0)
    score = sentiment_data.get("overall_score", 0)

    if pos_pct >= 65 or score >= 0.3:
        return {
            "verdict": "Strong Recommend",
            "label": "Highly Recommended ✅",
            "description": (
                "This creator enjoys overwhelmingly positive audience sentiment. "
                "An excellent candidate for brand collaboration."
            ),
            "color": "success",
            "positive_pct": pos_pct,
        }
    elif pos_pct >= 40 or score >= 0.05:
        return {
            "verdict": "Conditional Recommend",
            "label": "May Collaborate ⚠️",
            "description": (
                "Audience sentiment is moderate. Collaboration may work well if "
                "the creator's content aligns closely with your brand values."
            ),
            "color": "warning",
            "positive_pct": pos_pct,
        }
    else:
        return {
            "verdict": "Not Recommended",
            "label": "Not Recommended ❌",
            "description": (
                "This creator has predominantly negative or polarising audience sentiment. "
                "Collaboration carries significant reputational risk."
            ),
            "color": "danger",
            "positive_pct": pos_pct,
        }
