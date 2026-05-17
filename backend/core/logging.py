import logging
import sys
from typing import Any

from loguru import logger

from backend.core.config import Settings

CONSOLE_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
    "<level>{level: <8}</level> "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

FILE_LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level: <8} {name}:{line} | {message}"


class InterceptHandler(logging.Handler):
    """Forward standard-library logging records to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def init_logging(settings: Settings) -> Any:
    """Configure process-wide logging sinks."""

    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format=CONSOLE_LOG_FORMAT,
        enqueue=True,
    )

    if settings.log_to_file:
        settings.log_dir.mkdir(parents=True, exist_ok=True)
        logger.add(
            settings.log_dir / "{time:YYYY-MM-DD}.log",
            level=settings.log_level,
            format=FILE_LOG_FORMAT,
            encoding="utf-8",
            retention=settings.log_retention,
            rotation=settings.log_rotation,
            backtrace=True,
            diagnose=settings.log_diagnose,
            enqueue=True,
        )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(logger_name).handlers = [InterceptHandler()]

    return logger
