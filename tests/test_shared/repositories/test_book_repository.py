# Copyright 2024 BookWorm Inc. All rights reserved.

"""Tests for BookRepository."""

from unittest.mock import MagicMock, patch

import pytest


class TestBookRepository:
    """Test suite for BookRepository."""

    @patch("modules.shared.repositories.book_repository.DjangoBook")
    def test_get_by_id_found(self, mock_model, mock_book):
        """Test retrieving an existing book by ID."""
        from modules.shared.repositories.book_repository import BookRepository

        mock_model.objects.filter.return_value.get.return_value = mock_book

        repo = BookRepository()
        result = repo.get_by_id(1)

        assert result == mock_book
        mock_model.objects.filter.assert_called_once_with(is_deleted=False)

    @patch("modules.shared.repositories.book_repository.DjangoBook")
    def test_get_by_id_not_found(self, mock_model):
        """Test retrieving a non-existent book returns None."""
        from modules.shared.repositories.book_repository import BookRepository

        mock_model.DoesNotExist = Exception
        mock_model.objects.filter.return_value.get.side_effect = mock_model.DoesNotExist

        repo = BookRepository()
        result = repo.get_by_id(999)

        assert result is None

    @patch("modules.shared.repositories.book_repository.DjangoBook")
    def test_create_book(self, mock_model, mock_book):
        """Test creating a new book."""
        from modules.shared.repositories.book_repository import BookRepository

        mock_model.objects.create.return_value = mock_book

        repo = BookRepository()
        result = repo.create(title="Test", author="Author")

        assert result == mock_book
        mock_model.objects.create.assert_called_once_with(title="Test", author="Author")

    @patch("modules.shared.repositories.book_repository.DjangoBook")
    def test_list_books_default(self, mock_model):
        """Test listing books with default pagination."""
        from modules.shared.repositories.book_repository import BookRepository

        mock_qs = MagicMock()
        mock_model.objects.filter.return_value = mock_qs
        mock_qs.count.return_value = 2
        mock_qs.__getitem__ = MagicMock(return_value=[MagicMock(), MagicMock()])

        repo = BookRepository()
        books, total = repo.list_books()

        assert total == 2

    @patch("modules.shared.repositories.book_repository.DjangoBook")
    def test_delete_book(self, mock_model, mock_book):
        """Test soft-deleting a book."""
        from modules.shared.repositories.book_repository import BookRepository

        mock_model.objects.filter.return_value.get.return_value = mock_book

        repo = BookRepository()
        result = repo.delete(1)

        assert result is True
        mock_book.soft_delete.assert_called_once()
