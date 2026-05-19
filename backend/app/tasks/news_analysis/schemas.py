from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class NewsItem(BaseModel):
    """
    从新闻接口拿到的原始结构。
    """

    model_config = ConfigDict(populate_by_name=True)

    news_id: int = Field(alias="id")
    content: str
    publish_time: int = Field(alias="ctime")
    source_url: str = Field(alias="shareurl")


class ImpactDirection(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    UNCERTAIN = "uncertain"


class EventType(StrEnum):
    MACRO_POLICY = "宏观政策"
    INDUSTRY_POLICY = "行业政策"
    COMPANY_EVENT = "公司事件"
    INTERNATIONAL_EVENT = "国际事件"
    COMMODITY_PRICE = "商品价格"
    FINANCIAL_MARKET = "金融市场"
    REGULATION = "监管执法"
    EMERGENCY = "突发事件"
    OTHER = "其他"


class ScoreLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SectorImpact(BaseModel):
    sector: str = Field(description="受影响的行业或概念板块")
    impact: ImpactDirection = Field(description="对该板块的影响方向")
    reason: str = Field(description="判断该板块影响方向的原因")


class CompanyImpact(BaseModel):
    company: str = Field(description="新闻中明确提到或高度相关的公司名称")
    stock_code: str | None = Field(description="股票代码，只有新闻原文明确出现时填写，否则为 null")
    impact: ImpactDirection = Field(description="对该公司的影响方向")
    reason: str = Field(description="判断该公司影响方向的原因")


class NewsAnalysis(BaseModel):
    """
    AI 分析后的结构化数据。
    """

    news_id: int = Field(description="原始新闻 ID")
    summary: str = Field(description="一句话概括新闻内容")
    event_type: EventType = Field(description="新闻事件类型")
    market_impact: ImpactDirection = Field(description="对整体市场的影响方向")
    importance: ScoreLevel = Field(description="重要性等级（low/medium/high）")
    urgency: ScoreLevel = Field(description="紧急程度等级（low/medium/high）")
    sectors: list[SectorImpact] = Field(description="受影响板块列表")
    companies: list[CompanyImpact] = Field(description="受影响公司列表")
    reasoning: str = Field(description="简要分析逻辑")
    confidence: float = Field(description="置信度，范围 0 到 1")
