import tempfile
import unittest
from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from backend.api import endpoints_data
from backend.data.storage import FeatureStoreManager, normalize_stock_frame
from backend.main import app


class FeatureStoreTests(unittest.TestCase):
    def test_normalize_stock_frame_prefers_existing_lowercase_schema(self):
        raw = pd.DataFrame(
            {
                "Date": [pd.NaT],
                "Open": [None],
                "High": [None],
                "Low": [None],
                "Close": [None],
                "Volume": [None],
                "code": ["AAPL"],
                "trade_time": ["2026-05-11 09:30:00"],
                "open": [10.0],
                "high": [11.0],
                "low": [9.5],
                "close": [10.5],
                "volume": [1000],
            }
        )

        normalized = normalize_stock_frame(raw, "AAPL")

        self.assertEqual(
            normalized.columns.tolist(),
            ["code", "trade_time", "open", "high", "low", "close", "volume"],
        )
        self.assertEqual(len(normalized), 1)
        self.assertEqual(normalized.loc[0, "open"], 10.0)

    def test_append_and_read_normalizes_schema(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = FeatureStoreManager(Path(tmpdir))
            store.append_stock_data(
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

            stored = store.get_stock_data("MSFT")

            self.assertEqual(stored.loc[0, "code"], "MSFT")
            self.assertEqual(stored.loc[0, "close"], 20.5)
            self.assertEqual(stored.columns.tolist(), ["code", "trade_time", "open", "high", "low", "close", "volume"])


class DataApiTests(unittest.TestCase):
    def test_stock_endpoint_returns_json_safe_payload(self):
        client = TestClient(app)
        response = client.get("/api/v1/data/AAPL")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["ticker"], "AAPL")
        self.assertEqual(payload["count"], len(payload["data"]))
        if payload["data"]:
            self.assertEqual(
                sorted(payload["data"][0].keys()),
                ["close", "code", "high", "low", "open", "trade_time", "volume"],
            )

    def test_missing_stock_returns_empty_payload(self):
        original_store = endpoints_data.store_manager
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                endpoints_data.store_manager = FeatureStoreManager(Path(tmpdir))
                client = TestClient(app)
                response = client.get("/api/v1/data/NO_SUCH_TICKER")
        finally:
            endpoints_data.store_manager = original_store

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ticker": "NO_SUCH_TICKER", "count": 0, "data": []})


if __name__ == "__main__":
    unittest.main()
