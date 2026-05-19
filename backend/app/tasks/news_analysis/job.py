import asyncio
import json
import time

from app.core.logger import logger
from app.tasks.news_analysis.cls_telegraph_scraper import ClsTelegraphScraper
from app.tasks.news_analysis.exceptions import ClsScraperError
from app.tasks.news_analysis.llm import NewsLLMClient
from app.tasks.news_analysis.news_storage import AiAnalysisTable, NewsItemTable, NewsStorage


class MarketNewsMonitorJob:
    """
    抓取新闻 -> 过滤 -> AI分析 -> 入库的完整任务调度。
    作为应用层服务 (Service)，负责模型映射和业务流程编排。
    """

    def __init__(self, scraper: ClsTelegraphScraper, storage: NewsStorage, llm_client: NewsLLMClient):
        self.scraper = scraper
        self.storage = storage
        self.llm_client = llm_client

    def run_once(self) -> None:
        try:
            raw_items = self.scraper.get_latest_news()
            logger.info(f"本轮抓取财联社电报新闻数量: {len(raw_items)}")
        except ClsScraperError as e:
            logger.error(f"抓取新闻失败: {e}")
            return
        except Exception as e:
            logger.exception(f"抓取新闻出现未知异常: {e}")
            return

        # 业务层进行过滤
        candidate_ids = [item.news_id for item in raw_items]
        existing_ids = self.storage.get_existing_ids(candidate_ids)
        new_items = [item for item in raw_items if item.news_id not in existing_ids]

        if not new_items:
            logger.info("本轮没有新的新闻需要分析。")
            return

        logger.info(f"发现 {len(new_items)} 条全新新闻，开始进行 AI 分析。")

        for news in new_items:
            try:
                logger.info(f"开始分析新闻: {news.news_id}")
                analysis = self.llm_client.analyze(news)

                # 将 Pydantic 业务模型映射为 SQLModel 数据库模型
                raw_table = NewsItemTable(
                    news_id=news.news_id,
                    content=news.content,
                    publish_time=news.publish_time,
                    source_url=news.source_url,
                )

                ai_table = AiAnalysisTable(
                    news_id=analysis.news_id,
                    summary=analysis.summary,
                    event_type=analysis.event_type,
                    market_impact=analysis.market_impact,
                    importance=analysis.importance,
                    urgency=analysis.urgency,
                    sectors_json=json.dumps([s.model_dump() for s in analysis.sectors], ensure_ascii=False),
                    companies_json=json.dumps([c.model_dump() for c in analysis.companies], ensure_ascii=False),
                    reasoning=analysis.reasoning,
                    confidence=analysis.confidence,
                )

                # 存入数据库
                self.storage.save(raw_item=raw_table, ai_item=ai_table)

                logger.info(
                    f"分析及入库完成: news_id={analysis.news_id}, "
                    f"impact={analysis.market_impact}, "
                    f"importance={analysis.importance}, "
                    f"urgency={analysis.urgency}"
                )
                time.sleep(1)
            except Exception as e:
                logger.error(f"处理新闻失败: news_id={news.news_id}, error={e!r}")


async def run_market_news_monitor(
    scraper: ClsTelegraphScraper, storage: NewsStorage, llm_client: NewsLLMClient
) -> None:
    """
    提供给调度器的异步入口，内部通过线程池执行同步逻辑，防止阻塞事件循环。
    """
    job = MarketNewsMonitorJob(scraper=scraper, storage=storage, llm_client=llm_client)
    await asyncio.to_thread(job.run_once)


if __name__ == "__main__":
    from sqlmodel import create_engine

    from app.data.layout import get_local_data_layout

    layout = get_local_data_layout()
    db_path = layout.databases_dir / "news_storage.db"

    # 构建 SQLModel Engine
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url)

    scraper = ClsTelegraphScraper()
    storage = NewsStorage(engine=engine)
    llm_client = NewsLLMClient()
    job = MarketNewsMonitorJob(scraper=scraper, storage=storage, llm_client=llm_client)
    job.run_once()
