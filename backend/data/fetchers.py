from dataclasses import dataclass

from loguru import logger

from backend.data.market_bar_store import MarketBarStore
from backend.data.providers.base import MarketDataProvider


@dataclass(frozen=True)
class SyncResult:
    requested: int
    written: int
    skipped: int


def sync_stock_data(
    code_list: list[str],
    store: MarketBarStore,
    provider: MarketDataProvider,
    begin_date: int,
    end_date: int,
) -> SyncResult:
    """Fetch stock bars through a provider and persist them into the feature store."""
    snapshot_dict = provider.fetch_stock_bars(code_list, begin_date, end_date)

    written = 0
    skipped = 0
    for ticker in code_list:
        df = snapshot_dict.get(ticker)
        if df is None or df.empty:
            skipped += 1
            continue

        logger.info("Syncing data for {}, rows: {}", ticker, len(df))
        store.append_bars(ticker, df)
        written += 1

    return SyncResult(requested=len(code_list), written=written, skipped=skipped)
