from __future__ import annotations

import pandas as pd

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
    """Normalize imported stock bars to the local feature-store schema."""
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
        normalized["trade_time"] = normalized.index if isinstance(normalized.index, pd.DatetimeIndex) else pd.NaT

    normalized["trade_time"] = pd.to_datetime(normalized["trade_time"], errors="coerce")

    for column in NUMERIC_COLUMNS:
        if column not in normalized.columns:
            normalized[column] = pd.NA
        normalized[column] = pd.to_numeric(normalized[column], errors="coerce")

    normalized = normalized.dropna(subset=["trade_time"])
    normalized = normalized[STANDARD_COLUMNS]
    normalized = normalized.drop_duplicates(subset=["code", "trade_time"], keep="last")
    return normalized.sort_values(["code", "trade_time"]).reset_index(drop=True)


def dataframe_to_records(df: pd.DataFrame) -> list[dict]:
    """Convert a DataFrame to JSON-safe records for FastAPI responses."""
    if df.empty:
        return []

    safe_df = df.copy()
    for column in safe_df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
        safe_df[column] = safe_df[column].dt.strftime("%Y-%m-%dT%H:%M:%S")

    safe_df = safe_df.astype(object)
    safe_df = safe_df.where(pd.notna(safe_df), None)
    return safe_df.to_dict(orient="records")
