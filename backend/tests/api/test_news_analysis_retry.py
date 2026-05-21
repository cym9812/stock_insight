from pathlib import Path

from sqlalchemy.pool import NullPool
from sqlmodel import create_engine

from app.services.news_analysis_service import NewsAnalysisService
from app.tasks.news_analysis.exceptions import FetchError
from app.tasks.news_analysis.job import MarketNewsMonitorJob
from app.tasks.news_analysis.news_storage import AiAnalysisTable, AnalysisStatus, NewsItemTable, NewsStorage
from app.tasks.news_analysis.schemas import (
    EventType,
    ImpactDirection,
    NewsAnalysis,
    NewsItem,
    ScoreLevel,
)


class FakeScraper:
    def __init__(self, items: list[NewsItem] | None = None, fail: bool = False):
        self.items = items or []
        self.fail = fail

    def get_latest_news(self) -> list[NewsItem]:
        if self.fail:
            raise FetchError("fetch failed")
        return self.items


class FakeLLM:
    def __init__(self, outcomes: list[object]):
        self.outcomes = outcomes
        self.calls: list[int] = []

    def analyze(self, news: NewsItem) -> NewsAnalysis:
        self.calls.append(news.news_id)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def test_ai_failure_keeps_raw_news_pending_then_retries_successfully(tmp_path: Path):
    storage = make_storage(tmp_path)
    news = make_news_item(1)
    llm = FakeLLM([RuntimeError("temporary llm failure"), make_analysis(1)])
    job = MarketNewsMonitorJob(FakeScraper([news]), storage, llm)

    job.run_once()

    pending = storage.list_pending_items()
    assert [item.news_id for item in pending] == [1]
    assert pending[0].analysis_status == AnalysisStatus.PENDING.value
    assert pending[0].analysis_retry_count == 1

    job.run_once()

    pending = storage.list_pending_items()
    assert pending == []
    result = first_result(tmp_path)
    assert result.analysis_status == AnalysisStatus.ANALYZED.value
    assert result.summary == "summary"
    assert result.market_impact == ImpactDirection.POSITIVE.value
    assert llm.calls == [1, 1]


def test_ai_failure_marks_failed_after_retry_limit(tmp_path: Path):
    storage = make_storage(tmp_path)
    news = make_news_item(2)
    llm = FakeLLM([RuntimeError("fail 1"), RuntimeError("fail 2"), RuntimeError("fail 3")])
    job = MarketNewsMonitorJob(FakeScraper([news]), storage, llm)

    job.run_once()
    job.run_once()
    job.run_once()

    result = first_result(tmp_path)
    assert result.analysis_status == AnalysisStatus.FAILED.value
    assert result.analysis_retry_count == 3
    assert result.summary is None
    assert result.sectors == []


def test_fetch_failure_does_not_block_pending_retry(tmp_path: Path):
    storage = make_storage(tmp_path)
    storage.upsert_raw_items(
        [
            NewsItemTable(
                news_id=3,
                content="raw content",
                publish_time=1779200003,
                source_url="https://example.test/3",
            )
        ]
    )
    llm = FakeLLM([make_analysis(3)])
    job = MarketNewsMonitorJob(FakeScraper(fail=True), storage, llm)

    job.run_once()

    result = first_result(tmp_path)
    assert result.analysis_status == AnalysisStatus.ANALYZED.value
    assert result.summary == "summary"


def test_pending_news_is_visible_without_ai_fields(tmp_path: Path):
    storage = make_storage(tmp_path)
    storage.upsert_raw_items([make_raw_table(4)])

    result = first_result(tmp_path)

    assert result.news_id == 4
    assert result.analysis_status == AnalysisStatus.PENDING.value
    assert result.summary is None
    assert result.market_impact is None
    assert result.confidence is None
    assert result.sectors == []
    assert result.companies == []


def test_repeated_raw_upsert_does_not_reset_analysis_state(tmp_path: Path):
    storage = make_storage(tmp_path)
    storage.upsert_raw_items([make_raw_table(5)])
    storage.save_analysis_failure(5, "temporary failure")
    storage.upsert_raw_items([make_raw_table(5, content="updated raw content")])

    pending = storage.list_pending_items()
    assert pending[0].analysis_retry_count == 1
    assert pending[0].content == "updated raw content"

    storage.save_analysis_success(make_ai_table(5))
    storage.upsert_raw_items([make_raw_table(5, content="latest raw content")])

    result = first_result(tmp_path)
    assert result.analysis_status == AnalysisStatus.ANALYZED.value
    assert result.analysis_retry_count == 1
    assert result.summary == "summary"
    assert result.content == "latest raw content"


def make_storage(tmp_path: Path) -> NewsStorage:
    db_path = tmp_path / "news_storage.db"
    return NewsStorage(create_engine(f"sqlite:///{db_path}", poolclass=NullPool))


def first_result(tmp_path: Path):
    service = NewsAnalysisService(db_path=tmp_path / "news_storage.db")
    return service.list_results(limit=10).items[0]


def make_raw_table(news_id: int, content: str = "raw content") -> NewsItemTable:
    return NewsItemTable(
        news_id=news_id,
        content=content,
        publish_time=1779200000 + news_id,
        source_url=f"https://example.test/{news_id}",
    )


def make_news_item(news_id: int) -> NewsItem:
    return NewsItem(
        id=news_id,
        content="raw content",
        ctime=1779200000 + news_id,
        shareurl=f"https://example.test/{news_id}",
    )


def make_analysis(news_id: int) -> NewsAnalysis:
    return NewsAnalysis(
        news_id=news_id,
        summary="summary",
        event_type=EventType.OTHER,
        market_impact=ImpactDirection.POSITIVE,
        importance=ScoreLevel.HIGH,
        urgency=ScoreLevel.MEDIUM,
        sectors=[],
        companies=[],
        reasoning="reasoning",
        confidence=0.9,
    )


def make_ai_table(news_id: int) -> AiAnalysisTable:
    analysis = make_analysis(news_id)
    return AiAnalysisTable(
        news_id=analysis.news_id,
        summary=analysis.summary,
        event_type=analysis.event_type,
        market_impact=analysis.market_impact,
        importance=analysis.importance,
        urgency=analysis.urgency,
        sectors_json="[]",
        companies_json="[]",
        reasoning=analysis.reasoning,
        confidence=analysis.confidence,
    )
