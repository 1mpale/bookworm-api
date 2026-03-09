# Copyright 2024 BookWorm Inc. All rights reserved.

"""Repository for collection data access."""

import logging
from typing import Optional

from modules.shared.models.orm.models.django_collection import DjangoCollection

logger = logging.getLogger(__name__)


class CollectionRepository:
    """Data access layer for book collections.

    Provides CRUD operations for user-created book collections.
    """

    def get_by_id(self, collection_id: int) -> Optional[DjangoCollection]:
        """Retrieve a collection by its primary key.

        Args:
            collection_id: The collection's database ID.

        Returns:
            The collection instance, or None if not found.
        """
        try:
            return DjangoCollection.objects.filter(is_deleted=False).get(
                pk=collection_id
            )
        except DjangoCollection.DoesNotExist:
            return None

    def list_for_user(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> tuple[list[DjangoCollection], int]:
        """List collections owned by a user.

        Args:
            user_id: The user's database ID.
            page: Page number.
            page_size: Items per page.

        Returns:
            Tuple of (collections list, total count).
        """
        queryset = DjangoCollection.objects.filter(
            owner_id=user_id, is_deleted=False
        )
        total = queryset.count()
        offset = (page - 1) * page_size
        collections = list(queryset[offset : offset + page_size])
        return collections, total

    def create(self, **kwargs) -> DjangoCollection:
        """Create a new collection.

        Args:
            **kwargs: Collection field values.

        Returns:
            The created collection instance.
        """
        collection = DjangoCollection.objects.create(**kwargs)
        logger.info("Created collection: %s", collection.name)
        return collection

    def add_book(self, collection_id: int, book_id: int) -> bool:
        """Add a book to a collection.

        Args:
            collection_id: The collection's database ID.
            book_id: The book's database ID.

        Returns:
            True if added, False if collection not found.
        """
        collection = self.get_by_id(collection_id)
        if not collection:
            return False

        collection.books.add(book_id)
        logger.info("Added book %s to collection %s", book_id, collection_id)
        return True

    def remove_book(self, collection_id: int, book_id: int) -> bool:
        """Remove a book from a collection.

        Args:
            collection_id: The collection's database ID.
            book_id: The book's database ID.

        Returns:
            True if removed, False if collection not found.
        """
        collection = self.get_by_id(collection_id)
        if not collection:
            return False

        collection.books.remove(book_id)
        return True
