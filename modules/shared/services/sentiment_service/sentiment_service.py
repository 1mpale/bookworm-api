# Copyright 2024 BookWorm Inc. All rights reserved.

"""Sentiment analysis service for book reviews.

Uses a simple rule-based approach for sentiment scoring.
Can be extended with ML models for production use.
"""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# Sentiment word lists
POSITIVE_WORDS = {
    "excellent", "amazing", "wonderful", "fantastic", "brilliant", "outstanding",
    "superb", "great", "good", "enjoyable", "captivating", "compelling",
    "masterpiece", "riveting", "beautiful", "insightful", "engaging",
    "loved", "recommend", "favorite", "perfect", "delightful",
}

NEGATIVE_WORDS = {
    "terrible", "awful", "horrible", "boring", "dull", "disappointing",
    "waste", "poor", "bad", "mediocre", "confusing", "tedious",
    "predictable", "overrated", "disliked", "hated", "worst",
    "unreadable", "forgettable", "shallow",
}


class SentimentService:
    """Analyzes sentiment of book review text.

    Uses a lexicon-based approach to compute sentiment scores
    ranging from -1.0 (very negative) to 1.0 (very positive).
    """

    def __init__(self) -> None:
        """Initialize sentiment service with word lists."""
        self._positive_words = POSITIVE_WORDS
        self._negative_words = NEGATIVE_WORDS

    def analyze(self, text: str) -> float:
        """Compute sentiment score for a text.

        Args:
            text: The review text to analyze.

        Returns:
            Sentiment score between -1.0 and 1.0.
        """
        if not text or not text.strip():
            logger.debug("Empty text provided for sentiment analysis")
            return 0.0

        words = self._tokenize(text)
        if not words:
            return 0.0

        positive_count = sum(1 for w in words if w in self._positive_words)
        negative_count = sum(1 for w in words if w in self._negative_words)

        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            return 0.0

        score = (positive_count - negative_count) / total_sentiment_words
        logger.debug(
            "Sentiment analysis: %s positive, %s negative, score=%s",
            positive_count,
            negative_count,
            score,
        )
        return round(score, 4)

    def classify(self, score: float) -> str:
        """Classify a sentiment score into a category.

        Args:
            score: Sentiment score between -1.0 and 1.0.

        Returns:
            Classification string: 'positive', 'negative', or 'neutral'.
        """
        if score > 0.2:
            return "positive"
        elif score < -0.2:
            return "negative"
        return "neutral"

    def batch_analyze(self, texts: list[str]) -> list[Optional[float]]:
        """Analyze sentiment for multiple texts.

        Args:
            texts: List of text strings to analyze.

        Returns:
            List of sentiment scores (None for invalid texts).
        """
        results = []
        for text in texts:
            try:
                score = self.analyze(text)
                results.append(score)
            except Exception:
                logger.error(
                    "Failed to analyze sentiment for text",
                    exc_info=True,
                )
                results.append(None)

        logger.info("Batch sentiment analysis: processed %s texts", len(texts))
        return results

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into lowercase words.

        Args:
            text: Input text.

        Returns:
            List of lowercase word tokens.
        """
        text = text.lower()
        words = re.findall(r'\b[a-z]+\b', text)
        return words
