# Copyright 2024 BookWorm Inc. All rights reserved.

"""Seed the database with sample data for development."""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orm import configure_orm


SAMPLE_BOOKS = [
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "9780743273565",
        "genre": "Fiction",
        "description": "A story of the fabulously wealthy Jay Gatsby.",
    },
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "isbn": "9780061120084",
        "genre": "Fiction",
        "description": "The story of racial injustice and the loss of innocence.",
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935",
        "genre": "Dystopian",
        "description": "A dystopian social science fiction novel.",
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "genre": "Technology",
        "description": "A handbook of agile software craftsmanship.",
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "9780441013593",
        "genre": "Science Fiction",
        "description": "Set in the distant future amidst a feudal interstellar society.",
    },
]

SAMPLE_USERS = [
    {
        "email": "alice@example.com",
        "username": "alice",
        "password_hash": "$2b$12$LJ3m4ys4dSxGqM/pO.hash1",
        "display_name": "Alice Johnson",
        "role": "admin",
    },
    {
        "email": "bob@example.com",
        "username": "bob",
        "password_hash": "$2b$12$LJ3m4ys4dSxGqM/pO.hash2",
        "display_name": "Bob Smith",
        "role": "user",
    },
    {
        "email": "charlie@example.com",
        "username": "charlie",
        "password_hash": "$2b$12$LJ3m4ys4dSxGqM/pO.hash3",
        "display_name": "Charlie Brown",
        "role": "user",
    },
]


def seed() -> None:
    """Seed the database with sample data."""
    configure_orm()

    from modules.shared.models.orm.models.django_book import DjangoBook
    from modules.shared.models.orm.models.django_user import DjangoUser

    print("Seeding books...")
    for book_data in SAMPLE_BOOKS:
        book, created = DjangoBook.objects.get_or_create(
            isbn=book_data["isbn"], defaults=book_data
        )
        status = "created" if created else "exists"
        print(f"  {book.title}: {status}")

    print("\nSeeding users...")
    for user_data in SAMPLE_USERS:
        user, created = DjangoUser.objects.get_or_create(
            username=user_data["username"], defaults=user_data
        )
        status = "created" if created else "exists"
        print(f"  {user.username}: {status}")

    print("\nSeeding complete!")


if __name__ == "__main__":
    seed()
