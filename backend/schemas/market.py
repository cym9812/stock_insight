from pydantic import BaseModel


class MarketSentimentResponse(BaseModel):
    score: int
    label: str
    description: str


class MarketIndexItem(BaseModel):
    name: str
    value: str
    change: str
    data: list[float]


class HeatmapItem(BaseModel):
    name: str
    value: float
    change: float
