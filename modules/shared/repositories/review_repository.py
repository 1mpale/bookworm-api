# Copyright 2024 BookWorm Inc. All rights reserved.

"""Repository for review data access."""

import logging
from typing import Optional

from django.db.models import Avg, QuerySet

from modules.shared.models.orm.models.django_review import DjangoReview

logger = logging.getLogger(__name__)


class ReviewRepository:
    """Data access layer for reviews.

    Provides CRUD operations and query methods for the reviews table.
    """

    def get_by_id(self, review_id: int) -> Optional[DjangoReview]:
        """Retrieve a review by its primary key.

        Args:
            review_id: The review's database ID.

        Returns:
            The review instance, or None if not found.
        """
        try:
            return DjangoReview.objects.filter(is_deleted=False).get(pk=review_id)
        except DjangoReview.DoesNotExist:
            return None

    def list_for_book(
        self, book_id: int, page: int = 1, page_size: int = 20
    ) -> tuple[list[DjangoReview], int]:
        """List reviews for a specific book.

        Args:
            book_id: The book's database ID.
            page: Page number (1-indexed).
            page_size: Items per page.

        Returns:
            Tuple of (reviews list, total count).
        """
        queryset = DjangoReview.objects.filter(book_id=book_id, is_deleted=False)
        total = queryset.count()
        offset = (page - 1) * page_size
        reviews = list(queryset[offset : offset + page_size])

        logger.info(f"Listed {len(reviews)} reviews for book {book_id}")
        return reviews, total

    def create(self, **kwargs) -> DjangoReview:
        """Create a new review.

        Args:
            **kwargs: Review field values.

        Returns:
            The created review instance.
        """
        review = DjangoReview.objects.create(**kwargs)
        logger.info("Created review %s for book %s", review.pk, review.book_id)
        return review

    def update(self, review_id: int, **kwargs) -> Optional[DjangoReview]:
        """Update an existing review.

        Args:
            review_id: The review's database ID.
            **kwargs: Fields to update.

        Returns:
            The updated review, or None if not found.
        """
        review = self.get_by_id(review_id)
        if not review:
            return None

        for field, value in kwargs.items():
            setattr(review, field, value)
        review.save()
        return review

    def delete(self, review_id: int) -> bool:
        """Soft-delete a review.

        Args:
            review_id: The review's database ID.

        Returns:
            True if deleted, False if not found.
        """
        review = self.get_by_id(review_id)
        if not review:
            return False

        review.soft_delete()
        return True

    def get_unprocessed(self, limit: int = 100) -> QuerySet:
        """Get reviews that haven't been processed for sentiment.

        Args:
            limit: Maximum number of reviews to return.

        Returns:
            QuerySet of unprocessed reviews.
        """
        return DjangoReview.objects.filter(
            sentiment_processed=False, is_deleted=False
        )[:limit]

    def get_average_rating(self, book_id: int) -> tuple[float, int]:
        """Calculate average rating for a book.

        Args:
            book_id: The book's database ID.

        Returns:
            Tuple of (average rating, review count).
        """
        result = DjangoReview.objects.filter(
            book_id=book_id, is_deleted=False
        ).aggregate(avg_rating=Avg("rating"))

        count = DjangoReview.objects.filter(
            book_id=book_id, is_deleted=False
        ).count()

        return result["avg_rating"] or 0.0, count
