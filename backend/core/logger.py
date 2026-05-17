import sys

from loguru import logger as loguru_logger

from backend.core.config import settings

# ---------------------------------------------------------------------------
# Formatting Templates
# ---------------------------------------------------------------------------

# Console Format: Optimized for human readability during local development.
# Utilizes ANSI color codes (<green>, <cyan>) to help developers quickly spot
# errors in a fast-scrolling terminal output.
CONSOLE_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
    "<level>{level}</level> | "
    "<cyan>{file}</cyan> - <cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# File Format: Optimized for machine parsing and log aggregation systems
# (e.g., ELK Stack: Elasticsearch, Logstash, Kibana, or Splunk).
# Strips all ANSI color codes to prevent pollution of the ingested plain-text data.
FILE_LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss.SSS} {level} | {file} - {function}:{line} | {message}"



def init_logger():
    """
    Bootstraps the global logging singleton.

    This function intercepts the standard python logging output, clears default
    handlers to prevent duplicate logs, and attaches our customized sinks (Console + File).

    Returns:
        loguru.Logger: The globally configured logger instance.
    """
    log_dir = settings.log.dir
    log_dir.mkdir(parents=True, exist_ok=True)

    # Dynamic filename template. Loguru automatically evaluates the {time} block during rotation.
    log_path = f"{log_dir}/{{time:YYYY-MM-DD}}.log"

    # Purge the default sys.stderr handler attached by loguru upon import
    loguru_logger.remove()

    # Sink 1: Standard Output (stdout) for Docker/Kubernetes log collectors
    loguru_logger.add(sys.stdout, level=settings.log.console_log_level, format=CONSOLE_LOG_FORMAT)

    # Sink 2: Persistent Disk Storage for historical auditing
    loguru_logger.add(
        log_path,
        level=settings.log.file_log_level,
        format=FILE_LOG_FORMAT,
        encoding="utf-8",
        retention=settings.log.retention,
        backtrace=True,  # Captures full stack traces across thread boundaries
        diagnose=settings.log.diagnose,  # Exposes local variable states in the traceback
        enqueue=True,  # Critical: Enables non-blocking asynchronous logging
        rotation=settings.log.rotation,
    )
    return loguru_logger


# Instantiate the singleton upon module initialization
logger = init_logger()
