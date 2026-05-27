from datetime import datetime

from pydantic import BaseModel, Field


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


class NewsAnalysisStats(BaseModel):
    positive: int = Field(description="利好新闻数")
    negative: int = Field(description="利空新闻数")
    neutral: int = Field(description="中性新闻数")
    pending: int = Field(description="待分析新闻数")
    failed: int = Field(description="分析失败新闻数")


class NewsAnalysisResultsResponse(BaseModel):
    items: list[NewsAnalysisResultItem]
    total_count: int = Field(description="满足过滤条件的新闻总条数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页返回的新闻条数")
    total_pages: int = Field(description="总页数")
    stats: NewsAnalysisStats = Field(description="时间过滤条件下的新闻分类统计计数")



