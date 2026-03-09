# Copyright 2024 BookWorm Inc. All rights reserved.

"""Search endpoints."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request

from modules.shared.services.search_service.search_service import SearchService
from modules.shared.services.auth.jwt_middleware import get_current_user
from modules.shared.models.jwt_models import UserClaims

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Search"])
_search_service = SearchService()


@router.get("/search")
async def search_books(
    q: str = Query(..., min_length=1, max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """Search books by query string.

    Args:
        q: Search query.
        page: Page number.
        page_size: Items per page.
        user: Authenticated user claims.

    Returns:
        Search results with pagination.
    """
    logger.info(f"User {user.user_id} searching for: {q}")

    results = _search_service.search_books(q, page, page_size)
    total = _search_service.count_results(q)

    return {
        "items": results,
        "total": total,
        "page": page,
        "page_size": page_size,
        "query": q,
    }


@router.get("/search/suggestions")
async def get_suggestions(
    prefix: str = Query(..., min_length=1, max_length=100),
    limit: int = Query(10, ge=1, le=20),
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """Get search autocomplete suggestions.

    Args:
        prefix: The search prefix.
        limit: Maximum suggestions.
        user: Authenticated user claims.

    Returns:
        List of suggestions.
    """
    suggestions = _search_service.get_suggestions(prefix, limit)
    return {"suggestions": suggestions}
