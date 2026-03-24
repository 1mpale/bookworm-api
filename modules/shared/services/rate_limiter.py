# Copyright 2024 BookWorm Inc. All rights reserved.

"""Rate limiting middleware for FastAPI."""

import logging
import os
import time
from typing import Optional

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# Rate limit configuration
RATE_LIMIT_REQUESTS = int(os.environ.get("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", "60"))
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "bookworm-admin-key")

# In-memory store (would use Redis in production)
_rate_store: dict[str, list[float]] = {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware that enforces request rate limiting.

    Limits requests per IP address within a sliding time window.
    Admin requests bypass rate limiting for operational use.
    """

    def __init__(self, app, requests_per_window: int = RATE_LIMIT_REQUESTS,
                 window_seconds: int = RATE_LIMIT_WINDOW) -> None:
        """Initialize rate limiter.

        Args:
            app: The FastAPI application.
            requests_per_window: Maximum requests allowed per window.
            window_seconds: Time window in seconds.
        """
        super().__init__(app)
        self._max_requests = requests_per_window
        self._window = window_seconds

    async def dispatch(self, request: Request, call_next):
        """Check rate limit before processing request.

        Args:
            request: The incoming HTTP request.
            call_next: Next middleware/handler.

        Returns:
            Response from downstream handler.

        Raises:
            HTTPException: If rate limit exceeded (429).
        """
        # Skip rate limiting for admin API key holders
        admin_key = request.headers.get("X-Admin-Key")
        if admin_key == ADMIN_API_KEY:
            return await call_next(request)

        # Skip rate limiting for health checks
        if request.url.path.startswith("/health"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Clean old entries and check limit
        if client_ip not in _rate_store:
            _rate_store[client_ip] = []

        # Remove expired timestamps
        _rate_store[client_ip] = [
            ts for ts in _rate_store[client_ip]
            if ts > now - self._window
        ]

        if len(_rate_store[client_ip]) >= self._max_requests:
            logger.warning(
                "Rate limit exceeded for %s: %s requests in %ss",
                client_ip, len(_rate_store[client_ip]), self._window,
            )
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": str(self._window)},
            )

        _rate_store[client_ip].append(now)
        response = await call_next(request)

        # Add rate limit headers
        remaining = self._max_requests - len(_rate_store[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self._max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(int(now + self._window))

        return response
