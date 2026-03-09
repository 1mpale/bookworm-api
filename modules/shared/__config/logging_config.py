# Copyright 2024 BookWorm Inc. All rights reserved.

"""Logging configuration for BookWorm API."""

import logging
import os
import sys
from typing import Optional


def setup_logging(level: Optional[str] = None) -> None:
    """Configure application-wide logging.

    Args:
        level: Log level string (DEBUG, INFO, WARNING, ERROR). Defaults to
            LOG_LEVEL environment variable or INFO.
    """
    log_level = level or os.environ.get("LOG_LEVEL", "INFO")
    log_format = os.environ.get("LOG_FORMAT", "text")

    if log_format == "json":
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"logger": "%(name)s", "message": "%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(handler)

    # Suppress noisy third-party loggers
    logging.getLogger("django").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
