# Copyright 2024 BookWorm Inc. All rights reserved.

"""Background worker for processing review sentiment analysis."""

import logging
import time

from modules.shared.setup import initialize
from modules.shared.repositories.review_repository import ReviewRepository
from modules.shared.repositories.book_repository import BookRepository
from modules.shared.services.sentiment_service.sentiment_service import SentimentService

logger = logging.getLogger(__name__)


class SentimentWorker:
    """Background worker that processes review sentiment.

    Polls for unprocessed reviews and runs sentiment analysis,
    then updates the review records and book aggregate ratings.
    """

    def __init__(self) -> None:
        """Initialize worker with required services."""
        self._review_repo = ReviewRepository()
        self._book_repo = BookRepository()
        self._sentiment = SentimentService()
        self._batch_size = 50
        self._poll_interval = 30

    def run(self) -> None:
        """Start the worker loop.

        Continuously polls for unprocessed reviews and processes them.
        """
        logger.info("Sentiment worker started")

        while True:
            try:
                processed = self._process_batch()
                if processed == 0:
                    time.sleep(self._poll_interval)
            except KeyboardInterrupt:
                logger.info("Sentiment worker shutting down")
                break
            except Exception:
                logger.error("Sentiment worker error", exc_info=True)
                time.sleep(self._poll_interval)

    def _process_batch(self) -> int:
        """Process a batch of unprocessed reviews.

        Returns:
            Number of reviews processed.
        """
        reviews = self._review_repo.get_unprocessed(limit=self._batch_size)
        count = 0

        for review in reviews:
            try:
                score = self._sentiment.analyze(review.content)
                self._review_repo.update(
                    review.pk,
                    sentiment_score=score,
                    sentiment_processed=True,
                )

                # Update book aggregate rating
                avg, review_count = self._review_repo.get_average_rating(review.book_id)
                self._book_repo.update_rating(review.book_id, avg, review_count)

                count += 1
            except Exception:
                logger.error(
                    "Failed to process review %s", review.pk, exc_info=True
                )

        if count > 0:
            logger.info("Processed %s reviews for sentiment", count)

        return count


if __name__ == "__main__":
    initialize()
    worker = SentimentWorker()
    worker.run()
