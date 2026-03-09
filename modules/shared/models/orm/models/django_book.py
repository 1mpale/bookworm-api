# Copyright 2024 BookWorm Inc. All rights reserved.

"""Django ORM model for books."""

from django.db import models

from modules.shared.models.orm.models.django_base_model import DjangoBaseModel


class DjangoBook(DjangoBaseModel):
    """Book database model.

    Stores book metadata including title, author, ISBN, and genre.
    Maintains aggregate review statistics for efficient querying.
    """

    title = models.CharField(max_length=500, db_index=True)
    author = models.CharField(max_length=200, db_index=True)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    published_date = models.DateTimeField(null=True, blank=True)
    average_rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    embedding_vector = models.BinaryField(null=True, blank=True)

    class Meta:
        db_table = "books"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    __all__ = ["DjangoBook"]
