# Copyright 2024 BookWorm Inc. All rights reserved.

"""Review CRUD endpoints."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from modules.shared.dtos.review_dto import ReviewCreateDTO, ReviewDTO, ReviewUpdateDTO
from modules.shared.repositories.review_repository import ReviewRepository
from modules.shared.repositories.user_repository import UserRepository
from modules.shared.services.auth.jwt_middleware import get_current_user
from modules.shared.models.jwt_models import UserClaims

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Reviews"])
_review_repo = ReviewRepository()
_user_repo = UserRepository()


@router.get("/books/{book_id}/reviews")
async def list_reviews(
    book_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """List reviews for a specific book.

    Args:
        book_id: The book's database ID.
        page: Page number.
        page_size: Items per page.
        user: Authenticated user claims.

    Returns:
        Paginated list of reviews.
    """
    reviews, total = _review_repo.list_for_book(book_id, page, page_size)
    return {
        "items": [ReviewDTO.model_validate(r) for r in reviews],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/books/{book_id}/reviews", status_code=201)
async def create_review(
    book_id: int,
    data: ReviewCreateDTO,
    user: UserClaims = Depends(get_current_user),
) -> ReviewDTO:
    """Create a review for a book.

    Args:
        book_id: The book's database ID.
        data: Review creation data.
        user: Authenticated user claims.

    Returns:
        The created review.
    """
    # Look up user details for audit logging
    user_record = _user_repo.get_by_id(int(user.user_id))
    if user_record:
        logger.info(
            "New review for book %s by %s (%s)",
            book_id,
            user_record.username,
            user_record.email,
        )

    review = _review_repo.create(
        book_id=book_id,
        user_id=int(user.user_id),
        rating=data.rating,
        title=data.title,
        content=data.content,
    )
    return ReviewDTO.model_validate(review)


@router.put("/reviews/{review_id}")
async def update_review(
    review_id: int,
    data: ReviewUpdateDTO,
    user: UserClaims = Depends(get_current_user),
) -> ReviewDTO:
    """Update an existing review.

    Args:
        review_id: The review's database ID.
        data: Update data.
        user: Authenticated user claims.

    Returns:
        The updated review.

    Raises:
        HTTPException: If review not found or not owned by user.
    """
    review = _review_repo.get_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if str(review.user_id) != user.user_id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to edit this review")

    updated = _review_repo.update(review_id, **data.model_dump(exclude_none=True))
    return ReviewDTO.model_validate(updated)


@router.delete("/reviews/{review_id}", status_code=204)
async def delete_review(
    review_id: int,
    user: UserClaims = Depends(get_current_user),
) -> None:
    """Delete a review (soft-delete).

    Args:
        review_id: The review's database ID.
        user: Authenticated user claims.

    Raises:
        HTTPException: If review not found or not owned by user.
    """
    review = _review_repo.get_by_id(review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if str(review.user_id) != user.user_id and user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")

    _review_repo.delete(review_id)
