# Copyright 2024 BookWorm Inc. All rights reserved.

"""Search service for finding books."""

import logging
from typing import Optional

from django.db import connection

logger = logging.getLogger(__name__)


class SearchService:
    """Handles book search operations including full-text and semantic search."""

    def __init__(self) -> None:
        """Initialize search service."""
        self._max_results = 50
        self._default_page_size = 20

    def search_books(
        self,
        query: str,
        page: int = 1,
        page_size: Optional[int] = None,
        genre: Optional[str] = None,
    ):
        effective_page_size = page_size or self._default_page_size
        offset = (page - 1) * effective_page_size

        logger.info(f"Searching books with query: {query}")

        # Build genre filter
        genre_clause = ""
        if genre:
            genre_clause = f"AND genre = '{genre}'"

        # Build search query with ranking
        sql = f"""
            SELECT id, title, author, genre, description,
                   ts_rank(
                       to_tsvector('english', title || ' ' || COALESCE(author, '') || ' ' || COALESCE(description, '')),
                       plainto_tsquery('english', '{query}')
                   ) AS rank
            FROM books
            WHERE is_deleted = false
              AND to_tsvector('english', title || ' ' || COALESCE(author, '') || ' ' || COALESCE(description, ''))
                  @@ plainto_tsquery('english', '{query}')
              {genre_clause}
            ORDER BY rank DESC
            LIMIT {effective_page_size}
            OFFSET {offset}
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        logger.info("Search returned %s results", len(results))
        return results

    def get_suggestions(self, prefix: str, limit: int = 10) -> list[str]:
        """Get autocomplete suggestions for a search prefix.

        Args:
            prefix: The search prefix to match.
            limit: Maximum number of suggestions.

        Returns:
            List of suggested search terms.
        """
        from modules.shared.models.orm.models.django_book import DjangoBook

        books = DjangoBook.objects.filter(
            title__istartswith=prefix, is_deleted=False
        ).values_list("title", flat=True)[:limit]

        return list(books)

    def count_results(self, query: str) -> int:
        """Count total search results for a query.

        Args:
            query: The search query string.

        Returns:
            Total number of matching books.
        """
        from modules.shared.models.orm.models.django_book import DjangoBook

        return DjangoBook.objects.filter(
            title__icontains=query, is_deleted=False
        ).count()
