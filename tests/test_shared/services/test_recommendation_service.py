# Copyright 2024 BookWorm Inc. All rights reserved.

"""Tests for RecommendationService."""

from unittest.mock import MagicMock, patch

import pytest


class TestRecommendationService:
    """Test suite for RecommendationService."""

    @patch("modules.shared.services.recommendation_service.recommendation_service.CacheService")
    @patch("modules.shared.services.recommendation_service.recommendation_service.ReviewRepository")
    @patch("modules.shared.services.recommendation_service.recommendation_service.BookRepository")
    def test_get_recommendations_cached(self, mock_book_repo, mock_review_repo, mock_cache):
        """Test returning cached recommendations."""
        from modules.shared.services.recommendation_service.recommendation_service import (
            RecommendationService,
        )

        cached_data = [{"book_id": 1, "title": "Test"}]
        mock_cache_instance = MagicMock()
        mock_cache.return_value = mock_cache_instance
        mock_cache_instance.get.return_value = cached_data

        service = RecommendationService()
        result = service.get_recommendations(1)

        assert result == cached_data

    @patch("modules.shared.services.recommendation_service.recommendation_service.CacheService")
    @patch("modules.shared.services.recommendation_service.recommendation_service.ReviewRepository")
    @patch("modules.shared.services.recommendation_service.recommendation_service.BookRepository")
    def test_invalidate_cache(self, mock_book_repo, mock_review_repo, mock_cache):
        """Test cache invalidation."""
        from modules.shared.services.recommendation_service.recommendation_service import (
            RecommendationService,
        )

        mock_cache_instance = MagicMock()
        mock_cache.return_value = mock_cache_instance

        service = RecommendationService()
        service.invalidate_cache(1)

        mock_cache_instance.delete.assert_called_once_with("recommendations:1")
