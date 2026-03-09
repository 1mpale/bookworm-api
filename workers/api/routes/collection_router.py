# Copyright 2024 BookWorm Inc. All rights reserved.

"""Collection CRUD endpoints."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from modules.shared.repositories.collection_repository import CollectionRepository
from modules.shared.services.auth.jwt_middleware import get_current_user
from modules.shared.models.jwt_models import UserClaims

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Collections"])
_collection_repo = CollectionRepository()


class CollectionCreateDTO(BaseModel):
    """Collection creation request."""

    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    is_public: bool = False


class AddBookDTO(BaseModel):
    """Add book to collection request."""

    book_id: int


@router.get("/collections")
async def list_collections(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """List collections for the current user.

    Args:
        page: Page number.
        page_size: Items per page.
        user: Authenticated user claims.

    Returns:
        Paginated list of collections.
    """
    collections, total = _collection_repo.list_for_user(
        int(user.user_id), page, page_size
    )
    return {
        "items": [
            {
                "id": c.pk,
                "name": c.name,
                "description": c.description,
                "is_public": c.is_public,
            }
            for c in collections
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/collections", status_code=201)
async def create_collection(
    data: CollectionCreateDTO,
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """Create a new collection.

    Args:
        data: Collection creation data.
        user: Authenticated user claims.

    Returns:
        The created collection.
    """
    collection = _collection_repo.create(
        name=data.name,
        description=data.description,
        owner_id=int(user.user_id),
        is_public=data.is_public,
    )
    logger.info("Collection created: %s by user %s", collection.name, user.user_id)
    return {
        "id": collection.pk,
        "name": collection.name,
        "description": collection.description,
        "is_public": collection.is_public,
    }


@router.post("/collections/{collection_id}/books", status_code=201)
async def add_book_to_collection(
    collection_id: int,
    data: AddBookDTO,
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """Add a book to a collection.

    Args:
        collection_id: The collection's database ID.
        data: Book reference data.
        user: Authenticated user claims.

    Returns:
        Success message.

    Raises:
        HTTPException: If collection not found (404).
    """
    if not _collection_repo.add_book(collection_id, data.book_id):
        raise HTTPException(status_code=404, detail="Collection not found")

    return {"message": "Book added to collection"}
