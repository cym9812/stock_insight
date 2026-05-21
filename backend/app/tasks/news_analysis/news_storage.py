from datetime import UTC, datetime
from enum import StrEnum

from sqlmodel import Field, Session, SQLModel, col, select


class AnalysisStatus(StrEnum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    FAILED = "failed"


class NewsItemTable(SQLModel, table=True):
    __tablename__ = "news_items"

    news_id: int = Field(primary_key=True)
    content: str
    publish_time: int
    source_url: str
    analysis_status: str = Field(default=AnalysisStatus.PENDING.value, index=True)
    analysis_retry_count: int = Field(default=0)
    last_analysis_error: str | None = None
    last_analysis_attempt_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AiAnalysisTable(SQLModel, table=True):
    __tablename__ = "ai_analysis"

    news_id: int = Field(primary_key=True, foreign_key="news_items.news_id")
    summary: str
    event_type: str
    market_impact: str
    importance: str
    urgency: str
    sectors_json: str
    companies_json: str
    reasoning: str
    confidence: float


class NewsStorage:
    def __init__(self, engine):
        self.engine = engine
        SQLModel.metadata.create_all(self.engine)

    def upsert_raw_items(self, items: list[NewsItemTable]) -> int:
        if not items:
            return 0

        inserted_count = 0
        now = datetime.now(UTC)
        with Session(self.engine) as session:
            existing_ids = self._get_existing_ids(session, [item.news_id for item in items])
            for item in items:
                if item.news_id in existing_ids:
                    existing = session.get(NewsItemTable, item.news_id)
                    if existing is None:
                        continue
                    existing.content = item.content
                    existing.publish_time = item.publish_time
                    existing.source_url = item.source_url
                    existing.updated_at = now
                    continue

                item.created_at = now
                item.updated_at = now
                item.analysis_status = AnalysisStatus.PENDING.value
                item.analysis_retry_count = 0
                session.add(item)
                inserted_count += 1
            session.commit()
        return inserted_count

    def list_pending_items(self, limit: int = 50, max_retries: int = 3) -> list[NewsItemTable]:
        statement = (
            select(NewsItemTable)
            .where(NewsItemTable.analysis_status == AnalysisStatus.PENDING.value)
            .where(NewsItemTable.analysis_retry_count < max_retries)
            .order_by(NewsItemTable.publish_time.desc())
            .limit(limit)
        )

        with Session(self.engine) as session:
            return list(session.exec(statement).all())

    def mark_analyzing(self, news_id: int) -> None:
        now = datetime.now(UTC)
        with Session(self.engine) as session:
            item = session.get(NewsItemTable, news_id)
            if item is None:
                return
            item.analysis_status = AnalysisStatus.ANALYZING.value
            item.last_analysis_attempt_at = now
            item.updated_at = now
            session.add(item)
            session.commit()

    def save_analysis_success(self, ai_item: AiAnalysisTable) -> None:
        now = datetime.now(UTC)
        with Session(self.engine) as session:
            item = session.get(NewsItemTable, ai_item.news_id)
            if item is None:
                return

            existing_analysis = session.get(AiAnalysisTable, ai_item.news_id)
            if existing_analysis is None:
                session.add(ai_item)
            else:
                existing_analysis.summary = ai_item.summary
                existing_analysis.event_type = ai_item.event_type
                existing_analysis.market_impact = ai_item.market_impact
                existing_analysis.importance = ai_item.importance
                existing_analysis.urgency = ai_item.urgency
                existing_analysis.sectors_json = ai_item.sectors_json
                existing_analysis.companies_json = ai_item.companies_json
                existing_analysis.reasoning = ai_item.reasoning
                existing_analysis.confidence = ai_item.confidence

            item.analysis_status = AnalysisStatus.ANALYZED.value
            item.last_analysis_error = None
            item.updated_at = now
            session.add(item)
            session.commit()

    def save_analysis_failure(self, news_id: int, error: str, max_retries: int = 3) -> None:
        now = datetime.now(UTC)
        with Session(self.engine) as session:
            item = session.get(NewsItemTable, news_id)
            if item is None:
                return

            item.analysis_retry_count += 1
            item.analysis_status = (
                AnalysisStatus.FAILED.value
                if item.analysis_retry_count >= max_retries
                else AnalysisStatus.PENDING.value
            )
            item.last_analysis_error = error[:1000]
            item.updated_at = now
            session.add(item)
            session.commit()

    def get_existing_ids(self, news_ids: list[int]) -> set[int]:
        if not news_ids:
            return set()

        with Session(self.engine) as session:
            return self._get_existing_ids(session, news_ids)

    def _get_existing_ids(self, session: Session, news_ids: list[int]) -> set[int]:
        statement = select(NewsItemTable.news_id).where(col(NewsItemTable.news_id).in_(news_ids))
        results = session.exec(statement)
        return set(results.all())
