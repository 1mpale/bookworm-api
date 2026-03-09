# Copyright 2024 BookWorm Inc. All rights reserved.

"""Recommendation service for generating book recommendations."""

import logging
from typing import Optional

from modules.shared.repositories.book_repository import BookRepository
from modules.shared.repositories.review_repository import ReviewRepository
from modules.shared.services.cache_service.cache_service import CacheService

logger = logging.getLogger(__name__)

RECOMMENDATION_CACHE_TTL = 7200  # 2 hours


class RecommendationService:
    """Generates personalized book recommendations.

    Uses collaborative filtering based on user review history
    and book similarity scores.
    """

    def __init__(self) -> None:
        """Initialize recommendation service."""
        self._book_repo = BookRepository()
        self._review_repo = ReviewRepository()
        self._cache = CacheService()

    def get_recommendations(self, user_id, limit=10):
        cache_key = f"recommendations:{user_id}"
        cached = self._cache.get(cache_key)
        if cached:
            logger.info("Returning cached recommendations for user %s", user_id)
            return cached

        recommendations = self._compute_recommendations(user_id, limit)

        self._cache.set(cache_key, recommendations, ttl=RECOMMENDATION_CACHE_TTL)
        logger.info("Generated %s recommendations for user %s", len(recommendations), user_id)
        return recommendations

    def _compute_recommendations(self, user_id, limit):
        # Get books the user has reviewed highly
        from modules.shared.models.orm.models.django_review import DjangoReview

        user_reviews = DjangoReview.objects.filter(
            user_id=user_id, rating__gte=4, is_deleted=False
        ).select_related("book")

        if not user_reviews.exists():
            return self._get_popular_books(limit)

        # Find books with similar genres
        genres = set()
        reviewed_book_ids = set()
        for review in user_reviews:
            reviewed_book_ids.add(review.book_id)
            if review.book.genre:
                genres.add(review.book.genre)

        from modules.shared.models.orm.models.django_book import DjangoBook

        candidates = DjangoBook.objects.filter(
            genre__in=genres,
            is_deleted=False,
            average_rating__gte=3.5,
        ).exclude(pk__in=reviewed_book_ids).order_by("-average_rating")[:limit]

        return [
            {
                "book_id": book.pk,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "rating": book.average_rating,
                "reason": f"Based on your interest in {book.genre} books",
            }
            for book in candidates
        ]

    def _get_popular_books(self, limit):
        from modules.shared.models.orm.models.django_book import DjangoBook

        books = DjangoBook.objects.filter(
            is_deleted=False, review_count__gte=5
        ).order_by("-average_rating")[:limit]

        return [
            {
                "book_id": book.pk,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "rating": book.average_rating,
                "reason": "Popular and highly rated",
            }
            for book in books
        ]

    def invalidate_cache(self, user_id: int) -> None:
        """Invalidate recommendations cache for a user.

        Args:
            user_id: The user whose cache to invalidate.
        """
        self._cache.delete(f"recommendations:{user_id}")
        logger.info("Invalidated recommendations cache for user %s", user_id)

    def get_similar_books(self, book_id, limit=5):
        from modules.shared.models.orm.models.django_book import DjangoBook

        try:
            book = DjangoBook.objects.get(pk=book_id, is_deleted=False)
        except DjangoBook.DoesNotExist:
            return []

        similar = DjangoBook.objects.filter(
            genre=book.genre, is_deleted=False
        ).exclude(pk=book_id).order_by("-average_rating")[:limit]

        return [
            {
                "book_id": b.pk,
                "title": b.title,
                "author": b.author,
                "rating": b.average_rating,
            }
            for b in similar
        ]
