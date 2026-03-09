# Copyright 2024 BookWorm Inc. All rights reserved.

"""Shared test fixtures and configuration."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest


# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django ORM before any model imports
from orm import configure_orm
configure_orm()


@pytest.fixture
def mock_book():
    """Create a mock DjangoBook instance."""
    book = MagicMock()
    book.pk = 1
    book.title = "Test Book"
    book.author = "Test Author"
    book.isbn = "1234567890"
    book.genre = "Fiction"
    book.description = "A test book description"
    book.published_date = None
    book.average_rating = 4.5
    book.review_count = 10
    book.is_deleted = False
    book.created_at = "2024-01-01T00:00:00Z"
    book.updated_at = "2024-01-01T00:00:00Z"
    return book


@pytest.fixture
def mock_review():
    """Create a mock DjangoReview instance."""
    review = MagicMock()
    review.pk = 1
    review.book_id = 1
    review.user_id = 1
    review.rating = 5
    review.title = "Great book"
    review.content = "This is an excellent and amazing book that I absolutely loved"
    review.sentiment_score = 0.8
    review.sentiment_processed = True
    review.is_deleted = False
    review.created_at = "2024-01-01T00:00:00Z"
    review.updated_at = "2024-01-01T00:00:00Z"
    return review


@pytest.fixture
def mock_user():
    """Create a mock DjangoUser instance."""
    user = MagicMock()
    user.pk = 1
    user.email = "test@example.com"
    user.username = "testuser"
    user.display_name = "Test User"
    user.role = "user"
    user.is_active = True
    user.is_deleted = False
    return user
