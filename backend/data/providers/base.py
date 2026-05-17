from typing import Protocol

import pandas as pd


class MarketDataProvider(Protocol):
    """Interface for market data providers."""

    def fetch_stock_bars(self, tickers: list[str], begin_date: int, end_date: int) -> dict[str, pd.DataFrame]:
        """Fetch stock bars keyed by ticker."""
        ...
