# Copyright 2024 BookWorm Inc. All rights reserved.

"""Book data transfer objects."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BookDTO(BaseModel):
    """Book response model."""

    id: int
    title: str
    author: str
    isbn: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    published_date: Optional[datetime] = None
    average_rating: float = 0.0
    review_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookCreateDTO(BaseModel):
    """Book creation request model."""

    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$")
    genre: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
    published_date: Optional[datetime] = None


class BookUpdateDTO(BaseModel):
    """Book update request model."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, pattern=r"^\d{10}(\d{3})?$")
    genre: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
    published_date: Optional[datetime] = None


class BookListDTO(BaseModel):
    """Paginated book list response."""

    items: list[BookDTO]
    total: int
    page: int
    page_size: int
    pages: int
