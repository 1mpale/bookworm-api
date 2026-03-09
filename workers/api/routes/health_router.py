# Copyright 2024 BookWorm Inc. All rights reserved.

"""Health check endpoints."""

import logging

from fastapi import APIRouter

from modules.shared.services.client_service.clients.redis_client_manager import (
    RedisClientManager,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])
_redis = RedisClientManager()


@router.get("/health")
async def health_check() -> dict:
    """Basic health check.

    Returns:
        Health status.
    """
    return {"status": "healthy", "service": "bookworm-api"}


@router.get("/health/ready")
async def readiness_check() -> dict:
    """Readiness check including dependency health.

    Returns:
        Readiness status with dependency details.
    """
    redis_ok = _redis.health_check()

    status = "ready" if redis_ok else "degraded"
    return {
        "status": status,
        "dependencies": {
            "redis": "ok" if redis_ok else "unavailable",
        },
    }
