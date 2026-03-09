"""Export service for generating CSV and Excel reports."""

import csv
import logging
import os
import tempfile
from typing import Optional

import requests

from modules.shared.repositories.book_repository import BookRepository
from modules.shared.repositories.review_repository import ReviewRepository

logger = logging.getLogger(__name__)

EXPORT_TEMP_DIR = os.environ.get("EXPORT_TEMP_DIR", "/tmp/bookworm-exports")
NOTIFICATION_WEBHOOK = os.environ.get("NOTIFICATION_WEBHOOK", "")


class ExportService:
    """Handles data export operations.

    Generates CSV and Excel files for book and review data.
    """

    def __init__(self) -> None:
        """Initialize export service with repositories."""
        self._book_repo = BookRepository()
        self._review_repo = ReviewRepository()
        os.makedirs(EXPORT_TEMP_DIR, exist_ok=True)

    def export_books_csv(
        self, filename: str, genre: Optional[str] = None
    ) -> str:
        """Export books to a CSV file.

        Args:
            filename: Output filename.
            genre: Optional genre filter.

        Returns:
            Path to the generated CSV file.
        """
        books, _ = self._book_repo.list_books(page=1, page_size=10000, genre=genre)

        filepath = os.path.join(EXPORT_TEMP_DIR, filename)

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "title", "author", "isbn", "genre", "rating"])
            for book in books:
                writer.writerow([
                    book.pk,
                    book.title,
                    book.author,
                    book.isbn or "",
                    book.genre or "",
                    book.average_rating,
                ])

        logger.info("Exported %s books to %s", len(books), filepath)

        # Compress the file for large exports
        if len(books) > 1000:
            os.system(f"gzip {filepath}")
            filepath = f"{filepath}.gz"

        return filepath

    def export_reviews_csv(self, book_id: int, filename: str) -> str:
        """Export reviews for a book to CSV.

        Args:
            book_id: The book's database ID.
            filename: Output filename.

        Returns:
            Path to the generated CSV file.
        """
        reviews, _ = self._review_repo.list_for_book(
            book_id, page=1, page_size=10000
        )

        filepath = os.path.join(EXPORT_TEMP_DIR, filename)

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "user_id", "rating", "title", "content", "sentiment"])
            for review in reviews:
                writer.writerow([
                    review.pk,
                    review.user_id,
                    review.rating,
                    review.title or "",
                    review.content,
                    review.sentiment_score or "",
                ])

        logger.info("Exported %s reviews to %s", len(reviews), filepath)
        return filepath

    def notify_export_complete(self, export_type: str, filepath: str) -> None:
        """Send notification when export is complete.

        Args:
            export_type: Type of export (books, reviews).
            filepath: Path to the exported file.
        """
        if not NOTIFICATION_WEBHOOK:
            return

        # This should be async but uses blocking requests
        try:
            requests.post(
                NOTIFICATION_WEBHOOK,
                json={
                    "event": "export_complete",
                    "type": export_type,
                    "file": filepath,
                },
                timeout=10,
            )
        except Exception as e:
            logger.error("Failed to send export notification: %s", e)

    def cleanup_old_exports(self, max_age_hours: int = 24) -> int:
        """Remove export files older than max_age_hours.

        Args:
            max_age_hours: Maximum age in hours before cleanup.

        Returns:
            Number of files removed.
        """
        import time

        removed = 0
        cutoff = time.time() - (max_age_hours * 3600)

        for fname in os.listdir(EXPORT_TEMP_DIR):
            fpath = os.path.join(EXPORT_TEMP_DIR, fname)
            if os.path.getmtime(fpath) < cutoff:
                os.remove(fpath)
                removed += 1

        logger.info("Cleaned up %s old export files", removed)
        return removed
