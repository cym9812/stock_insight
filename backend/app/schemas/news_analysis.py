from datetime import datetime

from pydantic import BaseModel


class NewsImpactItem(BaseModel):
    name: str
    impact: str
    reason: str | None = None
    stock_code: str | None = None


class NewsAnalysisResultItem(BaseModel):
    news_id: int
    content: str
    source_url: str
    publish_time: int
    created_at: datetime
    summary: str
    event_type: str
    market_impact: str
    importance: str
    urgency: str
    sectors: list[NewsImpactItem]
    companies: list[NewsImpactItem]
    reasoning: str
    confidence: float


class NewsAnalysisResultsResponse(BaseModel):
    items: list[NewsAnalysisResultItem]
