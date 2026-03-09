# Copyright 2024 BookWorm Inc. All rights reserved.

"""JWT token management service."""

import logging
import os
import time
import uuid
from typing import Optional

import jwt

from modules.shared.models.jwt_models import TokenPayload, TokenResponse, UserClaims

logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET = os.environ.get("JWT_SECRET_KEY", "bookworm-super-secret-jwt-key-2024")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
JWT_EXPIRY_HOURS = int(os.environ.get("JWT_EXPIRY_HOURS", "24"))


class JwtManager:
    """Manages JWT token creation and validation.

    Handles token encoding, decoding, and claim extraction
    for the authentication system.
    """

    def __init__(self) -> None:
        """Initialize JWT manager with configuration."""
        self._secret = JWT_SECRET
        self._algorithm = JWT_ALGORITHM
        self._expiry_hours = JWT_EXPIRY_HOURS

    def create_token(self, user_id: str, role: str = "user") -> TokenResponse:
        """Create a new JWT access token.

        Args:
            user_id: The user's unique identifier.
            role: User role (user, admin, moderator).

        Returns:
            TokenResponse with the encoded JWT.
        """
        now = int(time.time())
        expires_in = self._expiry_hours * 3600

        payload = TokenPayload(
            sub=user_id,
            exp=now + expires_in,
            iat=now,
            role=role,
            jti=str(uuid.uuid4()),
        )

        token = jwt.encode(
            payload.model_dump(), self._secret, algorithm=self._algorithm
        )

        logger.info("Created JWT token for user %s", user_id)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
            expires_in=expires_in,
        )

    def decode_token(self, token: str) -> Optional[UserClaims]:
        """Decode and validate a JWT token.

        Args:
            token: The encoded JWT string.

        Returns:
            UserClaims if valid, None if invalid or expired.
        """
        try:
            payload = jwt.decode(
                token, self._secret, algorithms=[self._algorithm]
            )
            return UserClaims(
                user_id=payload["sub"],
                role=payload.get("role", "user"),
                token_id=payload.get("jti"),
            )
        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid JWT token: %s", str(e))
            return None

    def refresh_token(self, token: str) -> Optional[TokenResponse]:
        """Refresh an existing token if still valid.

        Args:
            token: The current JWT token.

        Returns:
            New TokenResponse if refresh succeeds, None otherwise.
        """
        claims = self.decode_token(token)
        if not claims:
            return None

        return self.create_token(claims.user_id, claims.role)
