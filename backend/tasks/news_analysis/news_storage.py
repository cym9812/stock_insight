from datetime import UTC, datetime

from sqlmodel import Field, Session, SQLModel, select


class NewsItemTable(SQLModel, table=True):
    __tablename__ = "news_items"

    news_id: int = Field(primary_key=True)
    title: str
    content: str
    publish_time: int
    source_url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AiAnalysisTable(SQLModel, table=True):
    __tablename__ = "ai_analysis"

    news_id: int = Field(primary_key=True, foreign_key="news_items.news_id")
    summary: str
    event_type: str
    market_impact: str
    importance: int
    urgency: int
    sectors_json: str
    companies_json: str
    reasoning: str
    confidence: float


class NewsStorage:
    """
    纯粹的仓储层 (Repository)：
    只负责与数据库交互，处理 SQLModel 对象，不感知上层 Pydantic 业务模型。
    """

    def __init__(self, engine):
        self.engine = engine
        # 确保表存在
        SQLModel.metadata.create_all(self.engine)

    def get_existing_ids(self, news_ids: list[int]) -> set[int]:
        """查询数据库，返回已存在的 news_id 集合"""
        if not news_ids:
            return set()
            
        with Session(self.engine) as session:
            statement = select(NewsItemTable.news_id).where(NewsItemTable.news_id.in_(news_ids))
            results = session.exec(statement)
            return set(results.all())

    def save(self, raw_item: NewsItemTable, ai_item: AiAnalysisTable) -> None:
        """保存原始新闻与 AI 分析结果（原子事务）"""
        with Session(self.engine) as session:
            session.add(raw_item)
            session.add(ai_item)
            # SQLModel (SQLAlchemy) session 自动包装在事务中
            # 如果中间报错，不会执行 commit，保证了一致性
            session.commit()
