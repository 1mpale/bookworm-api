# Copyright 2024 BookWorm Inc. All rights reserved.

"""Repository for book data access."""

import logging
from typing import Optional

from django.db.models import Q, QuerySet

from modules.shared.models.orm.models.django_book import DjangoBook

logger = logging.getLogger(__name__)


class BookRepository:
    """Data access layer for books.

    Provides CRUD operations and query methods for the books table.
    """

    def get_by_id(self, book_id: int) -> Optional[DjangoBook]:
        """Retrieve a book by its primary key.

        Args:
            book_id: The book's database ID.

        Returns:
            The book instance, or None if not found.
        """
        try:
            return DjangoBook.objects.filter(is_deleted=False).get(pk=book_id)
        except DjangoBook.DoesNotExist:
            logger.debug("Book not found: %s", book_id)
            return None

    def list_books(
        self,
        page: int = 1,
        page_size: int = 20,
        genre: Optional[str] = None,
        author: Optional[str] = None,
    ) -> tuple[list[DjangoBook], int]:
        """List books with pagination and optional filters.

        Args:
            page: Page number (1-indexed).
            page_size: Number of items per page.
            genre: Optional genre filter.
            author: Optional author name filter.

        Returns:
            Tuple of (books list, total count).
        """
        queryset = DjangoBook.objects.filter(is_deleted=False)

        if genre:
            queryset = queryset.filter(genre__iexact=genre)
        if author:
            queryset = queryset.filter(author__icontains=author)

        total = queryset.count()
        offset = (page - 1) * page_size
        books = list(queryset[offset : offset + page_size])

        logger.info("Listed %s books (page %s)", len(books), page)
        return books, total

    def create(self, **kwargs) -> DjangoBook:
        """Create a new book.

        Args:
            **kwargs: Book field values.

        Returns:
            The created book instance.
        """
        book = DjangoBook.objects.create(**kwargs)
        logger.info("Created book: %s (id=%s)", book.title, book.pk)
        return book

    def update(self, book_id: int, **kwargs) -> Optional[DjangoBook]:
        """Update an existing book.

        Args:
            book_id: The book's database ID.
            **kwargs: Fields to update.

        Returns:
            The updated book, or None if not found.
        """
        book = self.get_by_id(book_id)
        if not book:
            return None

        for field, value in kwargs.items():
            setattr(book, field, value)
        book.save()

        logger.info("Updated book %s", book_id)
        return book

    def delete(self, book_id: int) -> bool:
        """Soft-delete a book.

        Args:
            book_id: The book's database ID.

        Returns:
            True if deleted, False if not found.
        """
        book = self.get_by_id(book_id)
        if not book:
            return False

        book.soft_delete()
        logger.info("Deleted book %s", book_id)
        return True

    def search(self, query: str) -> QuerySet:
        """Search books by title, author, or description.

        Args:
            query: Search query string.

        Returns:
            QuerySet of matching books.
        """
        return DjangoBook.objects.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(description__icontains=query),
            is_deleted=False,
        )

    def update_rating(self, book_id: int, avg_rating: float, count: int) -> None:
        """Update a book's aggregate rating.

        Args:
            book_id: The book's database ID.
            avg_rating: New average rating.
            count: New review count.
        """
        DjangoBook.objects.filter(pk=book_id).update(
            average_rating=avg_rating, review_count=count
        )
