class StrategyService:
    def get_recommendations(self) -> dict:
        return {
            "date": "",
            "recommendations": [],
        }

    def get_backtest(self, strategy_id: str = "ai_daily") -> dict:
        return {
            "strategy_id": strategy_id,
            "returns": [],
            "benchmark": [],
            "dates": [],
        }
