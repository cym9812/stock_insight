from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlmodel import create_engine

from app.data.layout import get_local_data_layout
from app.tasks.news_analysis.cls_telegraph_scraper import ClsTelegraphScraper
from app.tasks.news_analysis.job import run_market_news_monitor
from app.tasks.news_analysis.llm import NewsLLMClient
from app.tasks.news_analysis.news_storage import NewsStorage


def register_jobs(scheduler: AsyncIOScheduler) -> None:
    """
    注册新闻分析模块的定时任务。
    
    该任务每 5 分钟执行一次，抓取财联社电报，过滤出新内容后调用 LLM 分析，并存入本地 SQLite。
    """
    # 依赖注入初始化
    layout = get_local_data_layout()
    db_path = layout.databases_dir / "news_storage.db"
    
    # 构建 SQLModel Engine
    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url)
    
    scraper = ClsTelegraphScraper()
    storage = NewsStorage(engine=engine)
    llm_client = NewsLLMClient()

    # 注册任务
    scheduler.add_job(
        run_market_news_monitor,
        trigger="interval",
        minutes=5,
        args=[scraper, storage, llm_client],
        id="market_news_monitor",
        name="Market News Scraper & AI Analysis",
        replace_existing=True,
    )
