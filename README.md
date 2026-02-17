# Project setup

## Run with Docker Compose

```bash
cp .env.example .env
docker compose up -d --build
```

## Alembic migrations

```bash
# create migration
alembic revision --autogenerate -m "init"

# apply migrations
alembic upgrade head

# rollback one migration
alembic downgrade -1
```

## Run tests

```bash
pytest -q
```

## Local backend start (optional)

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
