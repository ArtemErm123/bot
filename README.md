# Bot Monorepo Scaffold

Базовая структура монорепозитория для backend + frontend + infrastructure + docs.

## Структура

- `backend/` — FastAPI + SQLAlchemy + Alembic + tests.
- `frontend/` — React + TypeScript + Vite + UI kit + charts.
- `infra/` — docker-compose и шаблоны переменных окружения.
- `docs/` — архитектура, ERD, API-контракты.

## Модули A–H

- **A — API Gateway Layer**: HTTP-эндпоинты и роутинг (`backend/app/api`).
- **B — Application Services**: orchestration use-case логики (`backend/app/services`).
- **C — Domain Core**: доменные сущности/правила (`backend/app/domain`).
- **D — Repository Layer**: доступ к данным (`backend/app/repositories`).
- **E — Data Models**: SQLAlchemy ORM (`backend/app/models`).
- **F — Schemas/Contracts**: Pydantic DTO (`backend/app/schemas`).
- **G — Frontend UI**: клиентское приложение и визуализации (`frontend/src`).
- **H — Infrastructure & Docs**: compose/env и документация (`infra`, `docs`).

## Команды запуска

### Backend (локально)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (локально)

```bash
cd frontend
npm install
npm run dev
```

### В Docker Compose

```bash
cd infra
docker compose up --build
```

## Проверка backend-тестов

```bash
cd backend
pytest
```
