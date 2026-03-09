# BookWorm API — Endpoints

## Authentication

All endpoints except `/health` require a valid JWT token in the `Authorization: Bearer <token>` header.

## Endpoints

### Books

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/books` | List books (paginated) |
| GET | `/api/v1/books/{id}` | Get book by ID |
| POST | `/api/v1/books` | Create a new book |
| PUT | `/api/v1/books/{id}` | Update a book |
| DELETE | `/api/v1/books/{id}` | Delete a book |

### Reviews

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/books/{id}/reviews` | List reviews for a book |
| POST | `/api/v1/books/{id}/reviews` | Create a review |
| PUT | `/api/v1/reviews/{id}` | Update a review |
| DELETE | `/api/v1/reviews/{id}` | Delete a review |

### Search

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/search` | Search books by query |

### Collections

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/collections` | List user collections |
| POST | `/api/v1/collections` | Create a collection |
| PUT | `/api/v1/collections/{id}` | Update a collection |
| POST | `/api/v1/collections/{id}/books` | Add book to collection |

### Export

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/export/books` | Export books to CSV |
| POST | `/api/v1/export/reviews` | Export reviews to CSV |

### Admin

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/admin/stats` | System statistics |
| GET | `/api/v1/admin/audit-log` | Audit log entries |
| POST | `/api/v1/admin/cache/clear` | Clear cache |

### Health

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/health/ready` | Readiness check |

## Error Responses

All errors follow this format:

```json
{
  "detail": {
    "code": "NOT_FOUND",
    "message": "Book with id 123 not found"
  }
}
```

## Pagination

List endpoints support pagination:

```
GET /api/v1/books?page=1&page_size=20
```

Response includes:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```
