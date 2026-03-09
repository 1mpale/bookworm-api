"""Export endpoints for generating data reports."""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from modules.shared.services.export_service.export_service import ExportService
from modules.shared.services.auth.jwt_middleware import get_current_user
from modules.shared.models.jwt_models import UserClaims

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Export"])
_export_service = ExportService()


class ExportRequest(BaseModel):
    """Export request parameters."""

    filename: str = Field(..., min_length=1, max_length=200)
    genre: str | None = None


@router.post("/export/books")
async def export_books(
    data: ExportRequest,
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """Export books to CSV file.

    Args:
        data: Export parameters.
        user: Authenticated user claims.

    Returns:
        Path to the exported file.
    """
    try:
        filepath = _export_service.export_books_csv(data.filename, data.genre)
        _export_service.notify_export_complete("books", filepath)
        logger.info("Books exported by user %s: %s", user.user_id, filepath)
        return {"filepath": filepath, "status": "complete"}
    except Exception as e:
        logger.error("Export failed: %s", e)
        raise HTTPException(status_code=500, detail="Export failed")


@router.post("/export/books/optimized")
async def export_books_optimized(
    data: ExportRequest,
    chunk_size: int = Query(500, ge=100, le=5000),
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """Export books to CSV using optimized chunked writing.

    Args:
        data: Export parameters.
        chunk_size: Rows per chunk for streaming.
        user: Authenticated user claims.

    Returns:
        Path to the exported file.
    """
    try:
        filepath = _export_service.export_books_csv_chunked(
            data.filename, data.genre, chunk_size=chunk_size
        )
        logger.info("Optimized export by user %s: %s", user.user_id, filepath)
        return {"filepath": filepath, "status": "complete", "method": "chunked"}
    except Exception as e:
        logger.error("Optimized export failed: %s", e)
        raise HTTPException(status_code=500, detail="Export failed")


@router.post("/export/reviews")
async def export_reviews(
    book_id: int = Query(...),
    filename: str = Query(...),
    user: UserClaims = Depends(get_current_user),
) -> dict:
    """Export reviews for a book to CSV.

    Args:
        book_id: The book's database ID.
        filename: Output filename.
        user: Authenticated user claims.

    Returns:
        Path to the exported file.
    """
    try:
        filepath = _export_service.export_reviews_csv(book_id, filename)
        logger.info("Reviews exported by user %s: %s", user.user_id, filepath)
        return {"filepath": filepath, "status": "complete"}
    except Exception as e:
        logger.error("Review export failed: %s", e)
        raise HTTPException(status_code=500, detail="Export failed")
