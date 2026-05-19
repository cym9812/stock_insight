import json
from typing import Any

from sqlmodel import Session, SQLModel, create_engine, select

from app.data.layout import get_local_data_layout
from app.schemas.news_analysis import NewsAnalysisResultItem, NewsAnalysisResultsResponse, NewsImpactItem
from app.tasks.news_analysis.news_storage import AiAnalysisTable, NewsItemTable


class NewsAnalysisService:
    def list_results(self, limit: int = 50) -> NewsAnalysisResultsResponse:
        layout = get_local_data_layout()
        layout.ensure_directories()
        engine = create_engine(f"sqlite:///{layout.databases_dir / 'news_storage.db'}")
        SQLModel.metadata.create_all(engine)

        statement = (
            select(NewsItemTable, AiAnalysisTable)
            .join(AiAnalysisTable, NewsItemTable.news_id == AiAnalysisTable.news_id)
            .order_by(NewsItemTable.publish_time.desc())
            .limit(limit)
        )

        with Session(engine) as session:
            rows = session.exec(statement).all()

        return NewsAnalysisResultsResponse(
            items=[self._to_result_item(news_item, analysis_item) for news_item, analysis_item in rows]
        )

    def _to_result_item(
        self,
        news_item: NewsItemTable,
        analysis_item: AiAnalysisTable,
    ) -> NewsAnalysisResultItem:
        return NewsAnalysisResultItem(
            news_id=news_item.news_id,
            content=news_item.content,
            source_url=news_item.source_url,
            publish_time=news_item.publish_time,
            created_at=news_item.created_at,
            summary=analysis_item.summary,
            event_type=analysis_item.event_type,
            market_impact=analysis_item.market_impact,
            importance=analysis_item.importance,
            urgency=analysis_item.urgency,
            sectors=self._parse_impacts(analysis_item.sectors_json, name_key="sector"),
            companies=self._parse_impacts(analysis_item.companies_json, name_key="company"),
            reasoning=analysis_item.reasoning,
            confidence=analysis_item.confidence,
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
