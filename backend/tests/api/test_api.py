from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from app.api.v1 import stocks
from app.data.market_bar_store import MarketBarStore
from app.data.normalizers import normalize_stock_frame
from app.main import app
from app.services.stock_service import StockService


def test_normalize_stock_frame_prefers_existing_lowercase_schema():
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

    assert normalized.columns.tolist() == ["code", "trade_time", "open", "high", "low", "close", "volume"]
    assert len(normalized) == 1
    assert normalized.loc[0, "open"] == 10.0


def test_append_and_read_normalizes_schema(tmp_path: Path):
    store = MarketBarStore(tmp_path)
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

    assert stored.loc[0, "code"] == "MSFT"
    assert stored.loc[0, "close"] == 20.5
    assert stored.columns.tolist() == ["code", "trade_time", "open", "high", "low", "close", "volume"]


def test_stock_bars_endpoint_returns_json_safe_payload():
    client = TestClient(app)
    response = client.get("/api/v1/stocks/TEST/bars")

    assert response.status_code == 200
    payload = response.json()
    assert payload["ticker"] == "TEST"
    assert payload["count"] == len(payload["data"])
    if payload["data"]:
        assert {"code", "trade_time", "open", "high", "low", "close", "volume"} <= set(payload["data"][0])


def test_missing_stock_returns_empty_payload(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(stocks, "stock_service", StockService(MarketBarStore(tmp_path)))
    client = TestClient(app)

    response = client.get("/api/v1/stocks/NO_SUCH_TICKER/bars")

    assert response.status_code == 200
    assert response.json() == {"ticker": "NO_SUCH_TICKER", "count": 0, "data": []}


def test_business_routes_are_clean_and_available():
    client = TestClient(app)

    checks = [
        "/api/v1/stocks",
        "/api/v1/market/sentiment",
        "/api/v1/strategies/recommendations",
        "/api/v1/strategies/backtest",
        "/api/v1/portfolio/overview",
    ]

    for path in checks:
        assert client.get(path).status_code == 200
