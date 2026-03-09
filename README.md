# BookWorm API

A book management and recommendation platform.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-org/bookworm-api.git
cd bookworm-api
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Copy environment config:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run database migrations:
```bash
python orm.py migrate
```

6. Start the server:
```bash
uvicorn workers.api.main:app --host 0.0.0.0 --port 8080
```

### Docker

```bash
docker compose up --build
```

The API will be available at http://localhost:8080

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

## Testing

```bash
pytest tests/ -v --cov=modules
```

## Project Structure

See [Architecture Documentation](docs/architecture.md) for details.

## Contributing

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit a pull request
