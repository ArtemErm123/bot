from collections.abc import Callable
from typing import Generic, TypeVar

from pydantic import BaseModel

TCreate = TypeVar("TCreate", bound=BaseModel)
TModel = TypeVar("TModel", bound=BaseModel)


class InMemoryRepository(Generic[TCreate, TModel]):
    def __init__(self, factory: Callable[[int, TCreate], TModel]) -> None:
        self._store: dict[int, TModel] = {}
        self._next_id = 1
        self._factory = factory

    def list(self) -> list[TModel]:
        return list(self._store.values())

    def get(self, entity_id: int) -> TModel | None:
        return self._store.get(entity_id)

    def create(self, payload: TCreate) -> TModel:
        entity = self._factory(self._next_id, payload)
        self._store[self._next_id] = entity
        self._next_id += 1
        return entity

    def update(self, entity_id: int, payload: TCreate) -> TModel | None:
        if entity_id not in self._store:
            return None
        entity = self._factory(entity_id, payload)
        self._store[entity_id] = entity
        return entity

    def delete(self, entity_id: int) -> bool:
        return self._store.pop(entity_id, None) is not None
