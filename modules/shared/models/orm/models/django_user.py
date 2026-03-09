# Copyright 2024 BookWorm Inc. All rights reserved.

"""Django ORM model for users."""

from django.db import models

from modules.shared.models.orm.models.django_base_model import DjangoBaseModel


class DjangoUser(DjangoBaseModel):
    """User database model.

    Stores user account information and authentication data.
    """

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    display_name = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=[("user", "User"), ("admin", "Admin"), ("moderator", "Moderator")],
        default="user",
    )
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

    __all__ = ["DjangoUser"]
