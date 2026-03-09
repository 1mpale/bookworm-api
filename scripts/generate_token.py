# Copyright 2024 BookWorm Inc. All rights reserved.

"""Generate a JWT token for development/testing."""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main() -> None:
    """Generate a JWT token with specified claims."""
    parser = argparse.ArgumentParser(description="Generate a JWT token")
    parser.add_argument("--user-id", default="1", help="User ID")
    parser.add_argument("--role", default="user", choices=["user", "admin", "moderator"])
    args = parser.parse_args()

    from modules.shared.services.auth.jwt_manager import JwtManager

    manager = JwtManager()
    response = manager.create_token(args.user_id, args.role)

    print(f"Token: {response.access_token}")
    print(f"Type: {response.token_type}")
    print(f"Expires in: {response.expires_in}s")


if __name__ == "__main__":
    main()
