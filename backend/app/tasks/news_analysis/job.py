import asyncio
import json
import time

from app.core.logger import logger
from app.tasks.news_analysis.cls_telegraph_scraper import ClsTelegraphScraper
from app.tasks.news_analysis.exceptions import ClsScraperError
from app.tasks.news_analysis.llm import NewsLLMClient
from app.tasks.news_analysis.news_storage import AiAnalysisTable, NewsItemTable, NewsStorage
from app.tasks.news_analysis.schemas import NewsItem

MAX_ANALYSIS_RETRIES = 3
ANALYSIS_BATCH_LIMIT = 50


class MarketNewsMonitorJob:
    def __init__(self, scraper: ClsTelegraphScraper, storage: NewsStorage, llm_client: NewsLLMClient):
        self.scraper = scraper
        self.storage = storage
        self.llm_client = llm_client

    def run_once(self) -> None:
        self._fetch_and_store_raw_news()
        self._analyze_pending_news()

    def _fetch_and_store_raw_news(self) -> None:
        try:
            raw_items = self.scraper.get_latest_news()
        except ClsScraperError as exc:
            logger.error(f"Failed to fetch news: {exc}")
            return
        except Exception as exc:
            logger.exception(f"Unexpected news fetch error: {exc}")
            return

        raw_tables = [
            NewsItemTable(
                news_id=item.news_id,
                content=item.content,
                publish_time=item.publish_time,
                source_url=item.source_url,
            )
            for item in raw_items
        ]
        inserted_count = self.storage.upsert_raw_items(raw_tables)
        logger.info(f"Fetched {len(raw_items)} news items, inserted {inserted_count} new raw items.")

    def _analyze_pending_news(self) -> None:
        pending_items = self.storage.list_pending_items(
            limit=ANALYSIS_BATCH_LIMIT,
            max_retries=MAX_ANALYSIS_RETRIES,
        )
        if not pending_items:
            logger.info("No pending news items need AI analysis.")
            return

        logger.info(f"Analyzing {len(pending_items)} pending news items.")
        for news in pending_items:
            self._analyze_one(news)
            time.sleep(1)

    def _analyze_one(self, news: NewsItemTable) -> None:
        try:
            logger.info(f"Start AI analysis: news_id={news.news_id}")
            self.storage.mark_analyzing(news.news_id)
            analysis = self.llm_client.analyze(self._to_news_item(news))
            self.storage.save_analysis_success(
                AiAnalysisTable(
                    news_id=analysis.news_id,
                    summary=analysis.summary,
                    event_type=analysis.event_type,
                    market_impact=analysis.market_impact,
                    importance=analysis.importance,
                    urgency=analysis.urgency,
                    sectors_json=json.dumps([sector.model_dump() for sector in analysis.sectors], ensure_ascii=False),
                    companies_json=json.dumps(
                        [company.model_dump() for company in analysis.companies],
                        ensure_ascii=False,
                    ),
                    reasoning=analysis.reasoning,
                    confidence=analysis.confidence,
                )
            )
            logger.info(
                f"AI analysis completed: news_id={analysis.news_id}, "
                f"impact={analysis.market_impact}, importance={analysis.importance}, urgency={analysis.urgency}"
            )
        except Exception as exc:
            logger.error(f"AI analysis failed: news_id={news.news_id}, error={exc!r}")
            self.storage.save_analysis_failure(
                news_id=news.news_id,
                error=repr(exc),
                max_retries=MAX_ANALYSIS_RETRIES,
            )

    def _to_news_item(self, news: NewsItemTable) -> NewsItem:
        return NewsItem(
            id=news.news_id,
            content=news.content,
            ctime=news.publish_time,
            shareurl=news.source_url,
        )


async def run_market_news_monitor(
    scraper: ClsTelegraphScraper, storage: NewsStorage, llm_client: NewsLLMClient
) -> None:
    job = MarketNewsMonitorJob(scraper=scraper, storage=storage, llm_client=llm_client)
    await asyncio.to_thread(job.run_once)


if __name__ == "__main__":
    from sqlmodel import create_engine

    from app.data.layout import get_local_data_layout

    layout = get_local_data_layout()
    db_path = layout.databases_dir / "news_storage.db"
    engine = create_engine(f"sqlite:///{db_path}")

    scraper = ClsTelegraphScraper()
    storage = NewsStorage(engine=engine)
    llm_client = NewsLLMClient()
    job = MarketNewsMonitorJob(scraper=scraper, storage=storage, llm_client=llm_client)
    job.run_once()
