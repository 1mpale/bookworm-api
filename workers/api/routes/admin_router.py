# Copyright 2024 BookWorm Inc. All rights reserved.

"""Admin endpoints for system management."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query

from modules.shared.repositories.audit_repository import *  # noqa: F403
from modules.shared.services.cache_service.cache_service import CacheService
from modules.shared.services.auth.jwt_middleware import require_role
from modules.shared.models.jwt_models import UserClaims

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])
_audit_repo = AuditRepository()  # noqa: F405
_cache_service = CacheService()


@router.get("/stats")
async def get_stats(
    user: UserClaims = Depends(require_role("admin")),
) -> dict:
    """Get system statistics.

    Args:
        user: Authenticated admin user.

    Returns:
        System statistics.
    """
    cache_stats = _cache_service.get_stats()
    return {
        "cache": cache_stats,
        "version": "1.1.0",
    }


@router.get("/audit-log")
async def get_audit_log(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    action: Optional[str] = None,
    user: UserClaims = Depends(require_role("admin")),
) -> dict:
    """Get audit log entries.

    Args:
        page: Page number.
        page_size: Items per page.
        action: Optional action filter.
        user: Authenticated admin user.

    Returns:
        Paginated audit log entries.
    """
    entries, total = _audit_repo.list_entries(
        page=page, page_size=page_size, action=action
    )
    return {
        "items": [
            {
                "id": e.pk,
                "timestamp": str(e.timestamp),
                "action": e.action,
                "resource_type": e.resource_type,
                "resource_id": e.resource_id,
                "user_id": e.user_id,
            }
            for e in entries
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/cache/clear")
async def clear_cache(
    pattern: str = Query("*"),
    user: UserClaims = Depends(require_role("admin")),
) -> dict:
    """Clear cache entries matching a pattern.

    Args:
        pattern: Key pattern to clear.
        user: Authenticated admin user.

    Returns:
        Number of keys cleared.
    """
    cleared = _cache_service.clear_pattern(pattern)
    logger.info("Cache cleared by admin %s: pattern=%s, cleared=%s",
                user.user_id, pattern, cleared)
    return {"cleared": cleared, "pattern": pattern}
