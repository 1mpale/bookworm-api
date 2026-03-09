# Copyright 2024 BookWorm Inc. All rights reserved.

"""Abstract base model for all Django ORM models."""

from django.db import models


class DjangoBaseModel(models.Model):
    """Abstract base model providing common fields.

    All concrete models should inherit from this class to ensure
    consistent timestamps and soft-delete support.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Mark this record as deleted without removing from database."""
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
