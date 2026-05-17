from pydantic import BaseModel


class StockListResponse(BaseModel):
    stocks: list[str]


class StockBar(BaseModel):
    code: str | None
    trade_time: str | None
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    volume: float | None


class StockBarsResponse(BaseModel):
    ticker: str
    count: int
    data: list[StockBar]


class RadarAnalysis(BaseModel):
    indicators: list[str]
    values: list[float]


class StockAnalysisResponse(BaseModel):
    ticker: str
    radar: RadarAnalysis
    summary: str
    risks: list[str]
