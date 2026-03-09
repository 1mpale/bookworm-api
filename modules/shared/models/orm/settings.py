# Copyright 2024 BookWorm Inc. All rights reserved.

"""Django ORM application configuration."""

from django.apps import AppConfig


class SharedModelsConfig(AppConfig):
    """Django app config for shared ORM models."""

    name = "modules.shared.models.orm"
    label = "shared_models"
    verbose_name = "BookWorm Shared Models"
    default_auto_field = "django.db.models.BigAutoField"
