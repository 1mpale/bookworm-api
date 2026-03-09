# Copyright 2024 BookWorm Inc. All rights reserved.

"""Tests for SentimentService."""

import pytest

from modules.shared.services.sentiment_service.sentiment_service import SentimentService


class TestSentimentService:
    """Test suite for SentimentService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = SentimentService()

    def test_positive_text(self):
        """Test sentiment analysis of positive text."""
        text = "This book is excellent and amazing, truly a masterpiece"
        score = self.service.analyze(text)
        assert score > 0

    def test_negative_text(self):
        """Test sentiment analysis of negative text."""
        text = "This book is terrible and boring, a complete waste of time"
        score = self.service.analyze(text)
        assert score < 0

    def test_neutral_text(self):
        """Test sentiment analysis of neutral text."""
        text = "The book has pages and a cover with words inside"
        score = self.service.analyze(text)
        assert score == 0.0

    def test_empty_text(self):
        """Test sentiment analysis of empty text."""
        assert self.service.analyze("") == 0.0
        assert self.service.analyze("   ") == 0.0

    def test_classify_positive(self):
        """Test classification of positive score."""
        assert self.service.classify(0.5) == "positive"

    def test_classify_negative(self):
        """Test classification of negative score."""
        assert self.service.classify(-0.5) == "negative"

    def test_classify_neutral(self):
        """Test classification of neutral score."""
        assert self.service.classify(0.0) == "neutral"
        assert self.service.classify(0.1) == "neutral"
        assert self.service.classify(-0.1) == "neutral"

    def test_batch_analyze(self):
        """Test batch sentiment analysis."""
        texts = [
            "Excellent book, truly wonderful",
            "Terrible and boring",
            "It has pages",
        ]
        results = self.service.batch_analyze(texts)

        assert len(results) == 3
        assert results[0] > 0  # positive
        assert results[1] < 0  # negative
        assert results[2] == 0.0  # neutral
