from pydantic import BaseModel


class RecommendationItem(BaseModel):
    ticker: str
    prediction: str
    confidence: int
    reason: str


class RecommendationsResponse(BaseModel):
    date: str
    recommendations: list[RecommendationItem]


class BacktestResponse(BaseModel):
    strategy_id: str
    returns: list[float]
    benchmark: list[float]
    dates: list[str]
