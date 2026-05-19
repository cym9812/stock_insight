"""
示例定时任务。

在此模块中定义各类定时任务函数，并通过 register_jobs() 注册到调度器。
后续接入真实行情 SDK 后，可在此添加行情同步、指标计算等定时作业。
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger


async def heartbeat_job() -> None:
    """心跳任务：每分钟记录一次调度器运行状态，用于验证调度器正常工作。"""
    logger.debug("Scheduler heartbeat: running.")


async def example_data_sync_job() -> None:
    """占位数据同步任务：接入真实数据源后替换此实现。

    当前仅打印日志，不产生副作用。
    """
    logger.info("example_data_sync_job: placeholder, no real data source connected yet.")


def register_jobs(scheduler: AsyncIOScheduler) -> None:
    """将所有定时任务注册到调度器。

    Args:
        scheduler: 已初始化但尚未启动的 AsyncIOScheduler 实例。
    """
    # 心跳任务：每 1 分钟执行一次
    scheduler.add_job(
        heartbeat_job,
        trigger="interval",
        minutes=1,
        id="heartbeat",
        name="Scheduler Heartbeat",
        replace_existing=True,
    )

    # 占位数据同步任务：每天 09:00（Asia/Shanghai）执行一次
    scheduler.add_job(
        example_data_sync_job,
        trigger="cron",
        hour=9,
        minute=0,
        id="example_data_sync",
        name="Example Data Sync",
        replace_existing=True,
    )

    logger.info("Registered {} scheduled job(s).", 2)
