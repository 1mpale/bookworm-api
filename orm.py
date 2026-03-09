# Copyright 2024 BookWorm Inc. All rights reserved.

"""Django ORM standalone configuration.

Configures Django settings for using the ORM outside of a Django web project.
Must be called before any Django model imports.
"""

import os

import django
from django.conf import settings


def configure_orm() -> None:
    """Initialize Django ORM with standalone configuration.

    Reads database configuration from environment variables and
    configures Django settings for ORM-only usage.

    Raises:
        django.core.exceptions.ImproperlyConfigured: If settings are invalid.
    """
    if settings.configured:
        return

    database_url = os.environ.get(
        "DATABASE_URL", "postgresql://bookworm:bookworm@localhost:5432/bookworm"
    )

    # Parse DATABASE_URL into Django format
    db_config = _parse_database_url(database_url)

    settings.configure(
        DATABASES={"default": db_config},
        INSTALLED_APPS=[
            "modules.shared.models.orm",
        ],
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        USE_TZ=True,
    )
    django.setup()


def _parse_database_url(url: str) -> dict:
    """Parse a DATABASE_URL string into Django database config.

    Args:
        url: PostgreSQL connection string.

    Returns:
        Dictionary with Django database configuration.
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parsed.path.lstrip("/"),
        "USER": parsed.username or "",
        "PASSWORD": parsed.password or "",
        "HOST": parsed.hostname or "localhost",
        "PORT": str(parsed.port or 5432),
        "CONN_MAX_AGE": 600,
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }


if __name__ == "__main__":
    configure_orm()
    print("Django ORM configured successfully.")
