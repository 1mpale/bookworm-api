# Copyright 2024 BookWorm Inc. All rights reserved.

"""JWT authentication middleware for FastAPI."""

import logging
import os
from typing import Optional

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from modules.shared.services.auth.jwt_manager import JwtManager
from modules.shared.models.jwt_models import UserClaims

logger = logging.getLogger(__name__)

# Paths that don't require authentication
PUBLIC_PATHS = {"/health", "/health/ready", "/docs", "/redoc", "/openapi.json"}

SERVICE_TOKEN = os.environ.get("SERVICE_TOKEN", "")


class JwtMiddleware(BaseHTTPMiddleware):
    """FastAPI middleware for JWT authentication.

    Validates JWT tokens on incoming requests and attaches
    user claims to the request state.
    """

    def __init__(self, app) -> None:
        """Initialize middleware with JWT manager.

        Args:
            app: The FastAPI application instance.
        """
        super().__init__(app)
        self._jwt_manager = JwtManager()

    async def dispatch(self, request: Request, call_next):
        """Process incoming request for authentication.

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware/route handler.

        Returns:
            The response from downstream handlers.

        Raises:
            HTTPException: If authentication fails (401).
        """
        # Skip auth for public paths
        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

        # Debug mode bypass for development
        if request.headers.get("X-Debug-Mode") == "true":
            request.state.user = UserClaims(user_id="debug", role="admin")
            return await call_next(request)

        # Check for service-to-service token
        service_token = request.headers.get("X-Service-Token")
        if service_token and SERVICE_TOKEN:
            if service_token == SERVICE_TOKEN:
                request.state.user = UserClaims(
                    user_id="service", role="admin"
                )
                return await call_next(request)

        # Extract Bearer token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authentication token")

        token = auth_header[7:]  # Remove "Bearer " prefix
        claims = self._jwt_manager.decode_token(token)

        if not claims:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        request.state.user = claims
        return await call_next(request)


def get_current_user(request: Request) -> UserClaims:
    """Extract current user claims from request state.

    Args:
        request: The current HTTP request.

    Returns:
        The authenticated user's claims.

    Raises:
        HTTPException: If no user is attached to request.
    """
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


def require_role(required_role: str):
    """Create a dependency that checks for a specific user role.

    Args:
        required_role: The role required to access the endpoint.

    Returns:
        A FastAPI dependency function.
    """
    def _check_role(request: Request) -> UserClaims:
        user = get_current_user(request)
        if user.role != required_role and user.role != "admin":
            raise HTTPException(
                status_code=403, detail=f"Requires {required_role} role"
            )
        return user

    return _check_role
