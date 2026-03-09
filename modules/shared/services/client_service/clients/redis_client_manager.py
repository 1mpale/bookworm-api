# Copyright 2024 BookWorm Inc. All rights reserved.

"""Redis client manager for connection pooling."""

import logging
import os
from typing import Any

import redis

from modules.shared.services.client_service.clients.base_client_manager import (
    BaseClientManager,
)

logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")


class RedisClientManager(BaseClientManager):
    """Manages Redis client connections with connection pooling.

    Uses a singleton connection pool shared across instances.
    """

    _pool: Any = None

    def __init__(self) -> None:
        """Initialize Redis client manager."""
        super().__init__()
        if RedisClientManager._pool is None:
            RedisClientManager._pool = redis.ConnectionPool.from_url(
                REDIS_URL, max_connections=20, decode_responses=True
            )

    def get_client(self) -> redis.Redis:
        """Get a Redis client from the connection pool.

        Returns:
            A Redis client instance.
        """
        if self._client is None:
            self._client = redis.Redis(connection_pool=self._pool)
        return self._client

    def health_check(self) -> bool:
        """Check if Redis is reachable.

        Returns:
            True if Redis responds to ping.
        """
        try:
            client = self.get_client()
            return client.ping()
        except redis.ConnectionError:
            logger.error("Redis health check failed", exc_info=True)
            return False
