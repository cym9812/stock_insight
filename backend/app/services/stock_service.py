from app.data.market_bar_store import MarketBarStore
from app.data.normalizers import dataframe_to_records


class StockService:
    def __init__(self, store: MarketBarStore | None = None):
        self.store = store or MarketBarStore()

    def list_stocks(self) -> list[str]:
        return self.store.list_symbols()

    def get_stock_bars(self, ticker: str) -> dict:
        df = self.store.get_bars(ticker)
        return {
            "ticker": ticker,
            "count": len(df),
            "data": dataframe_to_records(df),
        }

    def get_stock_analysis(self, ticker: str) -> dict:
        return {
            "ticker": ticker,
            "radar": {
                "indicators": [],
                "values": [],
            },
            "summary": "暂无分析数据。",
            "risks": [],
        }
