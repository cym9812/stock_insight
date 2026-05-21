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
    analysis_status: str
    analysis_retry_count: int
    last_analysis_error: str | None = None
    summary: str | None = None
    event_type: str | None = None
    market_impact: str | None = None
    importance: str | None = None
    urgency: str | None = None
    sectors: list[NewsImpactItem]
    companies: list[NewsImpactItem]
    reasoning: str | None = None
    confidence: float | None = None


class NewsAnalysisResultsResponse(BaseModel):
    items: list[NewsAnalysisResultItem]
