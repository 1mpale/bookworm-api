# BookWorm API

## Architecture

BookWorm is a book management and recommendation platform built with:
- **FastAPI** for the REST API layer
- **Django ORM** (standalone, no Django web framework) for database access
- **Redis** for caching and session management
- **PostgreSQL** as the primary database
- **Background workers** for async processing (sentiment analysis, recommendations)

## Project Structure

```
bookworm-api/
├── configs/          # YAML configuration files
├── docs/             # Architecture and API documentation
├── modules/shared/   # Shared library (models, repos, services, DTOs)
├── workers/          # API server and background workers
├── tests/            # Test suite
└── scripts/          # Utility scripts
```

## Key Modules

- `modules/shared/models/orm/` — Django ORM models (Book, Review, User, Collection, AuditLog)
- `modules/shared/repositories/` — Data access layer (one repo per model)
- `modules/shared/services/` — Business logic services
- `modules/shared/dtos/` — Pydantic data transfer objects
- `workers/api/` — FastAPI application and route handlers
- `workers/background/` — Background task workers

## Coding Standards

### Copyright Headers
Every Python file MUST begin with:
```python
# Copyright 2024 BookWorm Inc. All rights reserved.
```

### Logging
- ALWAYS use lazy formatting with `%s` placeholders:
  ```python
  logger.info("Processing book %s", book_id)
  ```
- NEVER use f-strings in log messages:
  ```python
  # WRONG:
  logger.info(f"Processing book {book_id}")
  ```
- Exception logging MUST include `exc_info=True`:
  ```python
  logger.error("Failed to process book %s", book_id, exc_info=True)
  ```

### Type Hints
- All public function parameters and return types MUST have type hints
- Use `Optional[X]` for nullable types, `list[X]` for collections

### Imports
- No star imports (`from x import *`)
- No auto-import patterns in `__init__.py` (explicit imports only)
- Group imports: stdlib → third-party → local

### Async
- All I/O operations in async functions MUST be non-blocking
- Use `httpx` for async HTTP calls, `aiofiles` for file I/O
- Never use blocking `requests` or synchronous file I/O in async contexts

### Docstrings
- All public classes and functions MUST have Google-style docstrings
- Include Args, Returns, and Raises sections where applicable

### Security
- No hardcoded secrets — always use environment variables
- Use parameterized queries — never format SQL with string concatenation or f-strings
- Never log PII (emails, passwords, phone numbers, tokens)
- Use constant-time comparison for secret values (`hmac.compare_digest`)

### Testing
- Every service module must have corresponding test files
- Minimum 80% coverage target
- Tests mirror source structure: `tests/test_shared/services/`, `tests/test_workers/`
- Use pytest fixtures for common setup

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| REDIS_URL | Redis connection string | Yes |
| JWT_SECRET_KEY | Secret for JWT signing | Yes |
| EMBEDDING_API_KEY | API key for embedding service | Yes |
| LOG_LEVEL | Logging level (default: INFO) | No |

## Running

```bash
# Install dependencies
pip install -r requirements.txt

# Configure Django ORM
python orm.py

# Run API server
uvicorn workers.api.main:app --reload

# Run background workers
python -m workers.background.sentiment_worker
python -m workers.background.recommendation_worker

# Run tests
pytest tests/ -v
```
