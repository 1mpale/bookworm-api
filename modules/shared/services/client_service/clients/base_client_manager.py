# Copyright 2024 BookWorm Inc. All rights reserved.

"""Abstract base class for service client managers."""

import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class BaseClientManager(ABC):
    """Abstract base for managing service connections.

    Subclasses implement connection logic for specific backends
    (Redis, external APIs, etc.).
    """

    def __init__(self) -> None:
        """Initialize client manager."""
        self._client: Any = None

    @abstractmethod
    def get_client(self) -> Any:
        """Get or create a client connection.

        Returns:
            The connected client instance.
        """
        ...

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the client connection is healthy.

        Returns:
            True if the connection is healthy.
        """
        ...

    def close(self) -> None:
        """Close the client connection."""
        if self._client:
            logger.info("Closing %s client connection", self.__class__.__name__)
            self._client = None
