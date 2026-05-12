from pathlib import Path

import duckdb
import pandas as pd

from backend.config import settings

STANDARD_COLUMNS = ["code", "trade_time", "open", "high", "low", "close", "volume"]
NUMERIC_COLUMNS = ["open", "high", "low", "close", "volume"]
COLUMN_ALIASES = {
    "Date": "trade_time",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume",
}


def normalize_stock_frame(data: pd.DataFrame, ticker: str | None = None) -> pd.DataFrame:
    """
    Normalize imported stock data to the feature-store schema.
    """
    if data.empty:
        return pd.DataFrame(columns=STANDARD_COLUMNS)

    normalized = data.copy()

    for source, target in COLUMN_ALIASES.items():
        if source not in normalized.columns:
            continue
        if target in normalized.columns:
            normalized[target] = normalized[target].combine_first(normalized[source])
        else:
            normalized[target] = normalized[source]

    if "code" not in normalized.columns:
        normalized["code"] = ticker
    elif ticker:
        normalized["code"] = normalized["code"].fillna(ticker)

    if "trade_time" not in normalized.columns:
        if isinstance(normalized.index, pd.DatetimeIndex):
            normalized["trade_time"] = normalized.index
        else:
            normalized["trade_time"] = pd.NaT

    normalized["trade_time"] = pd.to_datetime(normalized["trade_time"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = pd.NA
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")

    normalized = normalized.dropna(subset=["trade_time"])
    normalized = normalized[STANDARD_COLUMNS]
    normalized = normalized.drop_duplicates(subset=["code", "trade_time"], keep="last")
    return normalized.sort_values(["code", "trade_time"]).reset_index(drop=True)


class FeatureStoreManager:
    def __init__(self, store_path: Path = settings.DATA_STORE_PATH):
        self.store_path = store_path
        self.store_path.mkdir(parents=True, exist_ok=True)
        # 初始化基于内存的 DuckDB 连接，后续可通过 SQL 直接查询 parquet
        self.conn = duckdb.connect(database=':memory:')

    def append_stock_data(self, ticker: str, new_data: pd.DataFrame):
        """
        全量覆盖或合并去重持久化为 Parquet 文件。
        """
        file_path = self.store_path / f"{ticker}.parquet"
        normalized_new = normalize_stock_frame(new_data, ticker)
        if file_path.exists():
            old_data = normalize_stock_frame(pd.read_parquet(file_path), ticker)
            combined = pd.concat([old_data, normalized_new], ignore_index=True)
            combined = normalize_stock_frame(combined, ticker)
            combined.to_parquet(file_path, index=False)
        else:
            normalized_new.to_parquet(file_path, index=False)

    def query_with_sql(self, sql_query: str) -> pd.DataFrame:
        """
        核心查询接口：使用 DuckDB 直接基于 SQL 查询所有 Parquet 文件
        例如：SELECT * FROM read_parquet('{STORE_PATH}/*.parquet') WHERE code = '...'
        """
        query = sql_query.replace("{STORE_PATH}", str(self.store_path))
        return self.conn.execute(query).df()

    def get_stock_data(self, ticker: str) -> pd.DataFrame:
        """为保持兼容，提供基础的单支股票读取接口"""
        file_path = self.store_path / f"{ticker}.parquet"
        if not file_path.exists():
            return pd.DataFrame(columns=STANDARD_COLUMNS)
        return normalize_stock_frame(pd.read_parquet(file_path), ticker)

    def list_stocks(self) -> list[str]:
        """返回所有存在缓存的股票代码列表"""
        files = list(self.store_path.glob("*.parquet"))
        return [f.stem for f in files]
