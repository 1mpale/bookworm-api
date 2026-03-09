# BookWorm API — Architecture

## Overview

BookWorm is a three-tier application:

1. **API Layer** (`workers/api/`) — FastAPI routes handling HTTP requests
2. **Service Layer** (`modules/shared/services/`) — Business logic
3. **Data Layer** (`modules/shared/repositories/` + `modules/shared/models/`) — Data access

## Service Map

| Service | Path | Description |
|---------|------|-------------|
| Auth | `modules/shared/services/auth/` | JWT authentication and middleware |
| Search | `modules/shared/services/search_service/` | Full-text and semantic search |
| Export | `modules/shared/services/export_service/` | CSV/Excel data export |
| Cache | `modules/shared/services/cache_service/` | Redis caching layer |
| NLP | `modules/shared/services/nlp_service/` | Sentiment analysis on reviews |
| Recommendations | `modules/shared/services/recommendation_service/` | Book recommendations |
| Notifications | `modules/shared/services/notification_service/` | Email and push notifications |
| Billing | `modules/shared/services/billing_service/` | Subscription management |

## Data Models

| Model | File | Table |
|-------|------|-------|
| DjangoBook | `django_book.py` | books |
| DjangoReview | `django_review.py` | reviews |
| DjangoUser | `django_user.py` | users |
| DjangoCollection | `django_collection.py` | collections |
| DjangoAuditLog | `django_audit_log.py` | audit_logs |
| DjangoTag | `django_tag.py` | tags |

## Background Workers

- **Sentiment Worker** — Processes new reviews through sentiment analysis
- **Recommendation Worker** — Updates book recommendations based on user activity
- **Notification Worker** — Sends queued notifications (email, push)

## Request Flow

```
Client → FastAPI Router → Service → Repository → Django ORM → PostgreSQL
                              ↓
                         Cache (Redis)
```

## Deployment

- Docker Compose for local development
- Kubernetes for production
- PostgreSQL 15 + Redis 7
