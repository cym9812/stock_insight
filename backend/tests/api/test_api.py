import tempfile
import unittest
from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from app.api.v1 import stocks
from app.data.market_bar_store import MarketBarStore
from app.data.normalizers import normalize_stock_frame
from app.main import app
from app.services.stock_service import StockService


class MarketBarStoreTests(unittest.TestCase):
    def test_normalize_stock_frame_prefers_existing_lowercase_schema(self):
        raw = pd.DataFrame(
            {
                "Date": [pd.NaT],
                "Open": [None],
                "High": [None],
                "Low": [None],
                "Close": [None],
                "Volume": [None],
                "code": ["TEST"],
                "trade_time": ["2026-05-11 09:30:00"],
                "open": [10.0],
                "high": [11.0],
                "low": [9.5],
                "close": [10.5],
                "volume": [1000],
            }
        )

        normalized = normalize_stock_frame(raw, "TEST")

        self.assertEqual(
            normalized.columns.tolist(),
            ["code", "trade_time", "open", "high", "low", "close", "volume"],
        )
        self.assertEqual(len(normalized), 1)
        self.assertEqual(normalized.loc[0, "open"], 10.0)

    def test_append_and_read_normalizes_schema(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = MarketBarStore(Path(tmpdir))
            store.append_bars(
                "MSFT",
                pd.DataFrame(
                    {
                        "Date": ["2026-05-11"],
                        "Open": [20],
                        "High": [21],
                        "Low": [19],
                        "Close": [20.5],
                        "Volume": [5000],
                    }
                ),
            )

            stored = store.get_bars("MSFT")

            self.assertEqual(stored.loc[0, "code"], "MSFT")
            self.assertEqual(stored.loc[0, "close"], 20.5)
            self.assertEqual(
                stored.columns.tolist(),
                ["code", "trade_time", "open", "high", "low", "close", "volume"],
            )


class ApiTests(unittest.TestCase):
    def test_stock_bars_endpoint_returns_json_safe_payload(self):
        client = TestClient(app)
        response = client.get("/api/v1/stocks/TEST/bars")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["ticker"], "TEST")
        self.assertEqual(payload["count"], len(payload["data"]))
        if payload["data"]:
            self.assertEqual(
                sorted(payload["data"][0].keys()),
                ["close", "code", "high", "low", "open", "trade_time", "volume"],
            )

    def test_missing_stock_returns_empty_payload(self):
        original_service = stocks.stock_service
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                stocks.stock_service = StockService(MarketBarStore(Path(tmpdir)))
                client = TestClient(app)
                response = client.get("/api/v1/stocks/NO_SUCH_TICKER/bars")
        finally:
            stocks.stock_service = original_service

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ticker": "NO_SUCH_TICKER", "count": 0, "data": []})

    def test_business_routes_are_clean_and_available(self):
        client = TestClient(app)

        checks = [
            "/api/v1/stocks",
            "/api/v1/market/sentiment",
            "/api/v1/strategies/recommendations",
            "/api/v1/strategies/backtest",
            "/api/v1/portfolio/overview",
        ]

        for path in checks:
            with self.subTest(path=path):
                self.assertEqual(client.get(path).status_code, 200)


if __name__ == "__main__":
    unittest.main()
