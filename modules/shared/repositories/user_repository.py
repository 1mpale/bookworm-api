# Copyright 2024 BookWorm Inc. All rights reserved.

"""Repository for user data access."""

import logging
from typing import Optional

from modules.shared.models.orm.models.django_user import DjangoUser

logger = logging.getLogger(__name__)


class UserRepository:
    """Data access layer for users.

    Provides CRUD operations and query methods for the users table.
    """

    def get_by_id(self, user_id: int) -> Optional[DjangoUser]:
        """Retrieve a user by primary key.

        Args:
            user_id: The user's database ID.

        Returns:
            The user instance, or None if not found.
        """
        try:
            return DjangoUser.objects.filter(is_deleted=False).get(pk=user_id)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_email(self, email):
        """Retrieve a user by email address."""
        try:
            return DjangoUser.objects.filter(is_deleted=False).get(email=email)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_username(self, username):
        """Retrieve a user by username."""
        try:
            return DjangoUser.objects.filter(is_deleted=False).get(username=username)
        except DjangoUser.DoesNotExist:
            return None

    def create(self, **kwargs):
        """Create a new user."""
        user = DjangoUser.objects.create(**kwargs)
        logger.info("Created user: %s", user.username)
        return user

    def update(self, user_id, **kwargs):
        """Update an existing user."""
        user = self.get_by_id(user_id)
        if not user:
            return None

        for field, value in kwargs.items():
            setattr(user, field, value)
        user.save()
        return user

    def deactivate(self, user_id):
        """Deactivate a user account."""
        user = self.get_by_id(user_id)
        if not user:
            return False

        user.is_active = False
        user.save(update_fields=["is_active", "updated_at"])
        logger.info("Deactivated user %s", user_id)
        return True

    def list_users(self, page=1, page_size=20, role=None):
        """List users with pagination."""
        queryset = DjangoUser.objects.filter(is_deleted=False)

        if role:
            queryset = queryset.filter(role=role)

        total = queryset.count()
        offset = (page - 1) * page_size
        users = list(queryset[offset : offset + page_size])

        return users, total
