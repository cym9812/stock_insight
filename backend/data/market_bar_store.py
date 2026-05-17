from pathlib import Path

import duckdb
import pandas as pd

from backend.data.layout import get_local_data_layout
from backend.data.normalizers import STANDARD_COLUMNS, normalize_stock_frame


class MarketBarStore:
    """Local Parquet storage for normalized market bar data."""

    def __init__(self, store_path: Path | None = None):
        layout = get_local_data_layout()
        layout.ensure_directories()
        self.store_path = store_path or layout.normalized_market_bars_dir
        self.store_path.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(database=":memory:")

    def append_bars(self, symbol: str, new_data: pd.DataFrame) -> None:
        """Merge market bars into the symbol parquet file after schema normalization."""
        file_path = self.store_path / f"{symbol}.parquet"
        normalized_new = normalize_stock_frame(new_data, symbol)

        if file_path.exists():
            old_data = normalize_stock_frame(pd.read_parquet(file_path), symbol)
            combined = pd.concat([old_data, normalized_new], ignore_index=True)
            normalized_new = normalize_stock_frame(combined, symbol)

        normalized_new.to_parquet(file_path, index=False)

    def query_with_sql(self, sql_query: str) -> pd.DataFrame:
        """Query market-bar parquet files through DuckDB."""
        query = sql_query.replace("{MARKET_BARS_PATH}", str(self.store_path))
        return self.conn.execute(query).df()

    def get_bars(self, symbol: str) -> pd.DataFrame:
        """Read one symbol's normalized market bars."""
        file_path = self.store_path / f"{symbol}.parquet"
        if not file_path.exists():
            return pd.DataFrame(columns=STANDARD_COLUMNS)
        return normalize_stock_frame(pd.read_parquet(file_path), symbol)

    def list_symbols(self) -> list[str]:
        """Return all symbols present in the local market-bar store."""
        return sorted(file_path.stem for file_path in self.store_path.glob("*.parquet"))
