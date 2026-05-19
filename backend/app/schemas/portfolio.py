from pydantic import BaseModel


class WatchlistItem(BaseModel):
    ticker: str
    price: float
    change: str
    suggestion: str


class HoldingItem(BaseModel):
    ticker: str
    avg_price: float
    current_price: float
    profit_pct: float


class PortfolioOverviewResponse(BaseModel):
    watchlist: list[WatchlistItem]
    holdings: list[HoldingItem]
