# Архитектура

Проект разделён на backend, frontend, infra и docs.

## Backend слойность

Backend соблюдает слоистую схему:

1. **API** (`app/api`) — маршруты и HTTP-граница.
2. **Services/Domain** (`app/services`, `app/domain`) — бизнес-правила и use-case логика.
3. **Repositories** (`app/repositories`) — доступ к данным и абстракции хранилищ.
4. **Models/Schemas** (`app/models`, `app/schemas`) — ORM-модели и DTO.

Поток зависимостей: `api -> services/domain -> repositories -> models/schemas`.
