# Copyright 2024 BookWorm Inc. All rights reserved.

"""Django ORM model for book collections."""

from django.db import models

from modules.shared.models.orm.models.django_base_model import DjangoBaseModel


class DjangoCollection(DjangoBaseModel):
    """Collection database model.

    Users can organize books into named collections (reading lists,
    favorites, etc.).
    """

    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        "shared_models.DjangoUser",
        on_delete=models.CASCADE,
        related_name="collections",
    )
    books = models.ManyToManyField(
        "shared_models.DjangoBook",
        related_name="collections",
        blank=True,
    )
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = "collections"
        ordering = ["-created_at"]
        unique_together = [("name", "owner")]

    def __str__(self) -> str:
        return f"{self.name} ({self.owner_id})"

    __all__ = ["DjangoCollection"]
