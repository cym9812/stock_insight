"""
定时任务调度器模块。

使用 APScheduler 的 AsyncIOScheduler，与 FastAPI asyncio 事件循环集成。
所有任务注册应在 start_scheduler() 调用前完成，或通过 scheduler 实例动态添加。
"""

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

# 全局 scheduler 实例
scheduler = AsyncIOScheduler(
    jobstores={
        "default": MemoryJobStore(),
    },
    executors={
        "default": AsyncIOExecutor(),
    },
    job_defaults={
        "coalesce": False,  # 错过执行不合并
        "max_instances": 1,  # 同一任务最多 1 个并发实例
        "misfire_grace_time": 60,  # 允许最多 60 秒延迟执行
    },
    timezone="Asia/Shanghai",
)


def start_scheduler() -> None:
    """启动调度器，并注册所有任务。"""
    from app.tasks.example_jobs import register_jobs

    register_jobs(scheduler)
    scheduler.start()
    logger.info("APScheduler started. Registered jobs: {}", len(scheduler.get_jobs()))


def shutdown_scheduler() -> None:
    """关闭调度器，等待所有正在运行的任务完成。"""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler shutdown complete.")
