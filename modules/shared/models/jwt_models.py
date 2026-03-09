# Copyright 2024 BookWorm Inc. All rights reserved.

"""JWT-related data models."""

from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str
    exp: int
    iat: int
    role: str = "user"
    jti: Optional[str] = None


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserClaims(BaseModel):
    """Extracted user claims from JWT."""

    user_id: str
    role: str
    token_id: Optional[str] = None
