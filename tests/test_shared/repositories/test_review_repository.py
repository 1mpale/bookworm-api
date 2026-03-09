# Copyright 2024 BookWorm Inc. All rights reserved.

"""Tests for ReviewRepository."""

from unittest.mock import MagicMock, patch

import pytest


class TestReviewRepository:
    """Test suite for ReviewRepository."""

    @patch("modules.shared.repositories.review_repository.DjangoReview")
    def test_get_by_id_found(self, mock_model, mock_review):
        """Test retrieving an existing review."""
        from modules.shared.repositories.review_repository import ReviewRepository

        mock_model.objects.filter.return_value.get.return_value = mock_review

        repo = ReviewRepository()
        result = repo.get_by_id(1)

        assert result == mock_review

    @patch("modules.shared.repositories.review_repository.DjangoReview")
    def test_create_review(self, mock_model, mock_review):
        """Test creating a new review."""
        from modules.shared.repositories.review_repository import ReviewRepository

        mock_model.objects.create.return_value = mock_review

        repo = ReviewRepository()
        result = repo.create(book_id=1, user_id=1, rating=5, content="Great")

        assert result == mock_review
        mock_model.objects.create.assert_called_once()

    @patch("modules.shared.repositories.review_repository.DjangoReview")
    def test_get_average_rating(self, mock_model):
        """Test calculating average rating for a book."""
        from modules.shared.repositories.review_repository import ReviewRepository

        mock_qs = MagicMock()
        mock_model.objects.filter.return_value = mock_qs
        mock_qs.aggregate.return_value = {"avg_rating": 4.2}
        mock_qs.count.return_value = 5

        repo = ReviewRepository()
        avg, count = repo.get_average_rating(1)

        assert avg == 4.2
        assert count == 5
