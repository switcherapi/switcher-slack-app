import logging

from src.utils.logging_config import (
    CONSOLE_HANDLER_NAME,
    DEFAULT_LOG_FORMAT,
    configure_logging,
    get_log_level,
)

def test_get_log_level_returns_default_for_invalid_value():
    assert get_log_level("not-a-level") == logging.INFO

def test_configure_logging_is_idempotent():
    root_logger = logging.getLogger()
    original_handlers = root_logger.handlers[:]
    original_level = root_logger.level

    try:
        root_logger.handlers = []

        configure_logging("DEBUG")
        configure_logging("INFO")

        matching_handlers = [
            handler
            for handler in root_logger.handlers
            if handler.get_name() == CONSOLE_HANDLER_NAME
        ]

        assert len(matching_handlers) == 1
        assert root_logger.level == logging.INFO
        assert matching_handlers[0].formatter is not None
        assert matching_handlers[0].formatter._fmt == DEFAULT_LOG_FORMAT
    finally:
        root_logger.handlers = original_handlers
        root_logger.setLevel(original_level)
