# Copyright 2024 BookWorm Inc. All rights reserved.

"""Shared configuration utilities."""

import os
from pathlib import Path
from typing import Any, Optional

import yaml


def load_yaml_config(config_name: str) -> dict[str, Any]:
    """Load a YAML configuration file from the configs directory.

    Args:
        config_name: Name of the config file (e.g., 'database', 'cache').

    Returns:
        Parsed YAML content as a dictionary.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
    """
    config_dir = Path(__file__).parent.parent.parent.parent / "configs"
    config_path = config_dir / f"{config_name}.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        return yaml.safe_load(f)


def get_env(key: str, default: Optional[str] = None, required: bool = False) -> str:
    """Get an environment variable with optional default.

    Args:
        key: Environment variable name.
        default: Default value if not set.
        required: If True, raise error when not set and no default.

    Returns:
        The environment variable value.

    Raises:
        ValueError: If required and not set.
    """
    value = os.environ.get(key, default)
    if value is None and required:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value or ""
