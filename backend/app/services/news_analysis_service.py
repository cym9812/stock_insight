import json
from pathlib import Path
from typing import Any

from sqlmodel import Session, SQLModel, create_engine, select

from app.data.layout import get_local_data_layout
from app.schemas.news_analysis import (
    NewsAnalysisResultItem,
    NewsAnalysisResultsResponse,
    NewsAnalysisStats,
    NewsImpactItem,
)
from app.tasks.news_analysis.news_storage import AiAnalysisTable, NewsItemTable


class NewsAnalysisService:
    def __init__(self, db_path: Path | None = None):
        self.db_path = db_path

    def list_results(
        self,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "priority",
        sort_dir: str = "desc",
        filter_type: str = "all",
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> NewsAnalysisResultsResponse:
        if limit is not None:
            page_size = limit

        layout = get_local_data_layout()
        layout.ensure_directories()
        db_path = self.db_path or layout.databases_dir / "news_storage.db"
        engine = create_engine(f"sqlite:///{db_path}")
        SQLModel.metadata.create_all(engine)

        from sqlalchemy import case, func
        from zoneinfo import ZoneInfo
        from datetime import datetime

        # Build base query
        base_query = (
            select(NewsItemTable, AiAnalysisTable)
            .join(AiAnalysisTable, NewsItemTable.news_id == AiAnalysisTable.news_id, isouter=True)
        )

        # Date Filters
        date_where_clauses = []
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=ZoneInfo("Asia/Shanghai"))
                start_ts = int(start_dt.timestamp())
                date_where_clauses.append(NewsItemTable.publish_time >= start_ts)
            except ValueError:
                pass
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59, tzinfo=ZoneInfo("Asia/Shanghai"))
                end_ts = int(end_dt.timestamp())
                date_where_clauses.append(NewsItemTable.publish_time <= end_ts)
            except ValueError:
                pass

        # Content/impact type filters
        where_clauses = list(date_where_clauses)
        if filter_type == "positive":
            where_clauses.append(AiAnalysisTable.market_impact == "positive")
        elif filter_type == "negative":
            where_clauses.append(AiAnalysisTable.market_impact == "negative")
        elif filter_type == "high":
            where_clauses.append((AiAnalysisTable.importance == "high") | (AiAnalysisTable.urgency == "high"))

        for clause in where_clauses:
            base_query = base_query.where(clause)

        # Count query
        count_query = select(func.count(NewsItemTable.news_id)).join(
            AiAnalysisTable, NewsItemTable.news_id == AiAnalysisTable.news_id, isouter=True
        )
        for clause in where_clauses:
            count_query = count_query.where(clause)

        # Stats query (Only filtered by date range, not by category)
        stats_query = (
            select(NewsItemTable.analysis_status, AiAnalysisTable.market_impact, func.count(NewsItemTable.news_id))
            .join(AiAnalysisTable, NewsItemTable.news_id == AiAnalysisTable.news_id, isouter=True)
            .group_by(NewsItemTable.analysis_status, AiAnalysisTable.market_impact)
        )
        for clause in date_where_clauses:
            stats_query = stats_query.where(clause)

        # Sorting
        importance_weight = case(
            (AiAnalysisTable.importance == "high", 3),
            (AiAnalysisTable.importance == "medium", 2),
            (AiAnalysisTable.importance == "low", 1),
            else_=1
        )
        urgency_weight = case(
            (AiAnalysisTable.urgency == "high", 3),
            (AiAnalysisTable.urgency == "medium", 2),
            (AiAnalysisTable.urgency == "low", 1),
            else_=1
        )
        priority_expr = (
            importance_weight * 26 +
            urgency_weight * 16 +
            func.coalesce(AiAnalysisTable.confidence, 0.0) * 18
        )

        if sort_by == "priority":
            if sort_dir == "asc":
                base_query = base_query.order_by(priority_expr.asc(), NewsItemTable.publish_time.asc())
            else:
                base_query = base_query.order_by(priority_expr.desc(), NewsItemTable.publish_time.desc())
        else:
            if sort_dir == "asc":
                base_query = base_query.order_by(NewsItemTable.publish_time.asc())
            else:
                base_query = base_query.order_by(NewsItemTable.publish_time.desc())

        # Pagination
        offset = (page - 1) * page_size
        base_query = base_query.limit(page_size).offset(offset)

        stats_data = {
            "positive": 0,
            "negative": 0,
            "neutral": 0,
            "pending": 0,
            "failed": 0
        }

        try:
            with Session(engine) as session:
                rows = session.exec(base_query).all()
                total = session.exec(count_query).one()
                stats_rows = session.exec(stats_query).all()
        finally:
            engine.dispose()

        for status, impact, count in stats_rows:
            if status in ("pending", "analyzing"):
                stats_data["pending"] += count
            elif status == "failed":
                stats_data["failed"] += count
            elif status == "analyzed":
                if impact == "positive":
                    stats_data["positive"] += count
                elif impact == "negative":
                    stats_data["negative"] += count
                else:
                    stats_data["neutral"] += count

        items = [self._to_result_item(news_item, analysis_item) for news_item, analysis_item in rows]
        pages = (total + page_size - 1) // page_size if total > 0 else 0

        return NewsAnalysisResultsResponse(
            items=items,
            total_count=total,
            page=page,
            page_size=page_size,
            total_pages=pages,
            stats=NewsAnalysisStats(**stats_data),
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
