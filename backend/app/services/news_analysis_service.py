import json
from pathlib import Path
from typing import Any

from sqlmodel import Session, SQLModel, create_engine, select

from app.data.layout import get_local_data_layout
from app.schemas.news_analysis import NewsAnalysisResultItem, NewsAnalysisResultsResponse, NewsImpactItem
from app.tasks.news_analysis.news_storage import AiAnalysisTable, NewsItemTable


class NewsAnalysisService:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path

    def list_results(self, limit: int = 50) -> NewsAnalysisResultsResponse:
        layout = get_local_data_layout()
        layout.ensure_directories()
        db_path = self.db_path or layout.databases_dir / "news_storage.db"
        engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(engine)

        statement = (
            select(NewsItemTable, AiAnalysisTable)
            .join(AiAnalysisTable, NewsItemTable.news_id == AiAnalysisTable.news_id, isouter=True)
            .order_by(NewsItemTable.publish_time.desc())
            .limit(limit)
        )

        try:
            with Session(engine) as session:
                rows = session.exec(statement).all()
        finally:
            engine.dispose()

        return NewsAnalysisResultsResponse(
            items=[self._to_result_item(news_item, analysis_item) for news_item, analysis_item in rows]
        )

    def _to_result_item(
        self,
        news_item: NewsItemTable,
        analysis_item: AiAnalysisTable | None,
    ) -> NewsAnalysisResultItem:
        return NewsAnalysisResultItem(
            news_id=news_item.news_id,
            content=news_item.content,
            source_url=news_item.source_url,
            publish_time=news_item.publish_time,
            created_at=news_item.created_at,
            analysis_status=news_item.analysis_status,
            analysis_retry_count=news_item.analysis_retry_count,
            last_analysis_error=news_item.last_analysis_error,
            summary=analysis_item.summary if analysis_item else None,
            event_type=analysis_item.event_type if analysis_item else None,
            market_impact=analysis_item.market_impact if analysis_item else None,
            importance=analysis_item.importance if analysis_item else None,
            urgency=analysis_item.urgency if analysis_item else None,
            sectors=self._parse_impacts(analysis_item.sectors_json, name_key="sector") if analysis_item else [],
            companies=self._parse_impacts(analysis_item.companies_json, name_key="company") if analysis_item else [],
            reasoning=analysis_item.reasoning if analysis_item else None,
            confidence=analysis_item.confidence if analysis_item else None,
        )

    def _parse_impacts(self, raw_value: str, name_key: str) -> list[NewsImpactItem]:
        try:
            parsed = json.loads(raw_value)
        except json.JSONDecodeError:
            return []

        if not isinstance(parsed, list):
            return []

        items: list[NewsImpactItem] = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            items.append(
                NewsImpactItem(
                    name=str(item.get(name_key) or item.get("name") or "-"),
                    impact=str(item.get("impact") or "neutral"),
                    reason=self._optional_str(item.get("reason")),
                    stock_code=self._optional_str(item.get("stock_code") or item.get("ticker")),
                )
            )
        return items

    def _optional_str(self, value: Any) -> str | None:
        if value is None:
            return None
        return str(value)
