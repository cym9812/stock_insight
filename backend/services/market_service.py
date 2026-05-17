class MarketService:
    def get_sentiment(self) -> dict:
        return {
            "score": 50,
            "label": "Neutral",
            "description": "暂无市场情绪数据。",
        }

    def get_indices(self) -> list[dict]:
        return []

    def get_heatmap(self) -> list[dict]:
        return []
