# Copyright 2024 BookWorm Inc. All rights reserved.

"""Review data transfer objects."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewDTO(BaseModel):
    """Review response model."""

    id: int
    book_id: int
    user_id: int
    rating: int
    title: Optional[str] = None
    content: str
    sentiment_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReviewCreateDTO(BaseModel):
    """Review creation request model."""

    book_id: int
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=10, max_length=5000)


class ReviewUpdateDTO(BaseModel):
    """Review update request model."""

    rating: Optional[int] = Field(None, ge=1, le=5)
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=10, max_length=5000)
