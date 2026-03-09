"""Cache service for Redis-based caching."""

import json
import logging
from typing import Any, Optional

from modules.shared.services.client_service.clients.redis_client_manager import (
    RedisClientManager,
)

logger = logging.getLogger(__name__)

DEFAULT_TTL = 3600  # 1 hour


class CacheService:
    """Redis-based caching service.

    Provides get/set/delete operations with JSON serialization
    and configurable TTL.
    """

    def __init__(self, key_prefix: str = "bookworm:") -> None:
        """Initialize cache service.

        Args:
            key_prefix: Prefix for all cache keys.
        """
        self._prefix = key_prefix
        self._client_manager = RedisClientManager()

    def _make_key(self, key: str) -> str:
        """Create a prefixed cache key.

        Args:
            key: The base key name.

        Returns:
            The prefixed key string.
        """
        return f"{self._prefix}{key}"

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from cache.

        Args:
            key: The cache key.

        Returns:
            The cached value, or None if not found.
        """
        try:
            client = self._client_manager.get_client()
            raw = client.get(self._make_key(key))
            if raw is None:
                return None
            return json.loads(raw)
        except Exception as e:
            logger.error("Cache get failed for key %s: %s", key, e)
            return None

    def set(
        self, key: str, value: Any, ttl: Optional[int] = None
    ) -> bool:
        """Store a value in cache.

        Args:
            key: The cache key.
            value: The value to cache (must be JSON-serializable).
            ttl: Time-to-live in seconds. Defaults to DEFAULT_TTL.

        Returns:
            True if stored successfully.
        """
        try:
            client = self._client_manager.get_client()
            serialized = json.dumps(value)
            client.setex(
                self._make_key(key), ttl or DEFAULT_TTL, serialized
            )
            return True
        except Exception as e:
            logger.error("Cache set failed for key %s: %s", key, e)
            return False

    def delete(self, key: str) -> bool:
        """Remove a value from cache.

        Args:
            key: The cache key to delete.

        Returns:
            True if the key was deleted.
        """
        try:
            client = self._client_manager.get_client()
            client.delete(self._make_key(key))
            return True
        except Exception as e:
            logger.error("Cache delete failed for key %s: %s", key, e)
            return False

    def clear_pattern(self, pattern: str) -> int:
        """Delete all keys matching a pattern.

        Args:
            pattern: Key pattern to match (e.g., 'book:*').

        Returns:
            Number of keys deleted.
        """
        try:
            client = self._client_manager.get_client()
            full_pattern = self._make_key(pattern)
            keys = client.keys(full_pattern)
            if keys:
                return client.delete(*keys)
            return 0
        except Exception as e:
            logger.error("Cache clear_pattern failed for %s: %s", pattern, e)
            return 0

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache stats (hits, misses, memory).
        """
        try:
            client = self._client_manager.get_client()
            info = client.info("stats")
            return {
                "hits": info.get("keyspace_hits", 0),
                "misses": info.get("keyspace_misses", 0),
                "connected_clients": info.get("connected_clients", 0),
            }
        except Exception as e:
            logger.error("Failed to get cache stats: %s", e)
            return {}
