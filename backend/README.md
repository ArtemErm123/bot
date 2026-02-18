# Backend

FastAPI backend scaffold with layered architecture.

## Основной entrypoint

Основным модулем для запуска и тестирования считается `app.main:app`.
Именно этот ASGI-объект агрегирует целевой API-контракт с префиксами `/api`, `/api/v1` и `/reports`.
