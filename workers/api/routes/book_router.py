# Copyright 2024 BookWorm Inc. All rights reserved.

"""Book CRUD endpoints."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from modules.shared.dtos.book_dto import (
    BookCreateDTO,
    BookDTO,
    BookListDTO,
    BookUpdateDTO,
)
from modules.shared.repositories.book_repository import BookRepository
from modules.shared.services.auth.jwt_middleware import get_current_user
from modules.shared.models.jwt_models import UserClaims

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Books"])
_book_repo = BookRepository()


@router.get("/books", response_model=BookListDTO)
async def list_books(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    genre: Optional[str] = None,
    author: Optional[str] = None,
    user: UserClaims = Depends(get_current_user),
) -> BookListDTO:
    """List books with pagination and optional filters.

    Args:
        request: The HTTP request.
        page: Page number.
        page_size: Items per page.
        genre: Optional genre filter.
        author: Optional author filter.
        user: Authenticated user claims.

    Returns:
        Paginated list of books.
    """
    books, total = _book_repo.list_books(
        page=page, page_size=page_size, genre=genre, author=author
    )
    pages = (total + page_size - 1) // page_size

    return BookListDTO(
        items=[BookDTO.model_validate(b) for b in books],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.get("/books/{book_id}", response_model=BookDTO)
async def get_book(
    book_id: int,
    user: UserClaims = Depends(get_current_user),
) -> BookDTO:
    """Get a book by ID.

    Args:
        book_id: The book's database ID.
        user: Authenticated user claims.

    Returns:
        The book details.

    Raises:
        HTTPException: If book not found (404).
    """
    book = _book_repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookDTO.model_validate(book)


@router.post("/books", response_model=BookDTO, status_code=201)
async def create_book(
    data: BookCreateDTO,
    user: UserClaims = Depends(get_current_user),
) -> BookDTO:
    """Create a new book.

    Args:
        data: Book creation data.
        user: Authenticated user claims.

    Returns:
        The created book.
    """
    book = _book_repo.create(**data.model_dump(exclude_none=True))
    logger.info("Book created by user %s: %s", user.user_id, book.pk)
    return BookDTO.model_validate(book)


@router.put("/books/{book_id}", response_model=BookDTO)
async def update_book(
    book_id: int,
    data: BookUpdateDTO,
    user: UserClaims = Depends(get_current_user),
) -> BookDTO:
    """Update an existing book.

    Args:
        book_id: The book's database ID.
        data: Update data.
        user: Authenticated user claims.

    Returns:
        The updated book.

    Raises:
        HTTPException: If book not found (404).
    """
    book = _book_repo.update(book_id, **data.model_dump(exclude_none=True))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info("Book %s updated by user %s", book_id, user.user_id)
    return BookDTO.model_validate(book)


@router.delete("/books/{book_id}", status_code=204)
async def delete_book(
    book_id: int,
    user: UserClaims = Depends(get_current_user),
) -> None:
    """Delete a book (soft-delete).

    Args:
        book_id: The book's database ID.
        user: Authenticated user claims.

    Raises:
        HTTPException: If book not found (404).
    """
    if not _book_repo.delete(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info("Book %s deleted by user %s", book_id, user.user_id)
