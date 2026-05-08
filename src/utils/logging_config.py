import logging

from typing import Optional
from utils.constants import LOG_LEVEL

DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] %(name)s: %(message)s"
DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"
CONSOLE_HANDLER_NAME = "switcher-console"
LOG_LEVELS = logging.getLevelNamesMapping()

def get_log_level(level_name: Optional[str] = None) -> int:
    """Resolve a configured log level name to a logging constant."""

    configured_level = (level_name or LOG_LEVEL).strip().upper()
    return LOG_LEVELS.get(configured_level, DEFAULT_LOG_LEVEL)

def configure_logging(level_name: Optional[str] = None) -> logging.Logger:
    """Configure process-wide console logging without adding duplicate handlers."""

    level = get_log_level(level_name)
    formatter = logging.Formatter(
        fmt = DEFAULT_LOG_FORMAT,
        datefmt = DEFAULT_LOG_DATE_FORMAT,
    )
    root_logger = logging.getLogger()

    if root_logger.handlers:
        for handler in root_logger.handlers:
            handler.setLevel(level)
            handler.setFormatter(formatter)
    else:
        handler = logging.StreamHandler()
        handler.set_name(CONSOLE_HANDLER_NAME)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    root_logger.setLevel(level)
    return root_logger
