# Copyright 2024 BookWorm Inc. All rights reserved.

"""Background worker for updating book recommendations."""

import logging
import time

from modules.shared.setup import initialize
from modules.shared.services.recommendation_service.recommendation_service import (
    RecommendationService,
)

logger = logging.getLogger(__name__)


class RecommendationWorker:
    """Background worker that refreshes recommendations.

    Periodically recomputes recommendations for active users
    to keep the cache warm.
    """

    def __init__(self) -> None:
        """Initialize worker with recommendation service."""
        self._recommendation_service = RecommendationService()
        self._refresh_interval = 3600  # 1 hour

    def run(self) -> None:
        """Start the worker loop.

        Periodically refreshes recommendations for active users.
        """
        logger.info("Recommendation worker started")

        while True:
            try:
                self._refresh_recommendations()
                time.sleep(self._refresh_interval)
            except KeyboardInterrupt:
                logger.info("Recommendation worker shutting down")
                break
            except Exception:
                logger.error("Recommendation worker error", exc_info=True)
                time.sleep(self._refresh_interval)

    def _refresh_recommendations(self) -> None:
        """Refresh recommendations for recently active users."""
        from modules.shared.models.orm.models.django_user import DjangoUser

        active_users = DjangoUser.objects.filter(
            is_active=True, is_deleted=False
        ).values_list("pk", flat=True)[:100]

        refreshed = 0
        for user_id in active_users:
            try:
                self._recommendation_service.invalidate_cache(user_id)
                self._recommendation_service.get_recommendations(user_id)
                refreshed += 1
            except Exception:
                logger.error(
                    "Failed to refresh recommendations for user %s",
                    user_id,
                    exc_info=True,
                )

        logger.info("Refreshed recommendations for %s users", refreshed)


if __name__ == "__main__":
    initialize()
    worker = RecommendationWorker()
    worker.run()
