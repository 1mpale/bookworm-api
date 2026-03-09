# Copyright 2024 BookWorm Inc. All rights reserved.

"""Shared module setup and initialization."""

import logging

from orm import configure_orm


logger = logging.getLogger(__name__)


def initialize() -> None:
    """Initialize shared module dependencies.

    Configures Django ORM and validates required settings.
    """
    logger.info("Initializing shared module")
    configure_orm()
    logger.info("Shared module initialized successfully")
