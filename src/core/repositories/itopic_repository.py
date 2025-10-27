from abc import ABC, abstractmethod
from typing import Any, Iterable
from src.core.domain.topic import Topic, TopicIn


class ITopicRepository:

    @abstractmethod
    async def get_all(self) -> Iterable[Any]:
        pass

    @abstractmethod
    async def get_by_id(self, id_topic: int) -> Any | None:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Any | None:
        pass

    @abstractmethod
    async def add(self, data: TopicIn) -> Any | None:
        pass

    @abstractmethod
    async def update(self, id_topic: int, data: TopicIn) -> Any | None:
        pass

    @abstractmethod
    async def delete(self, id_topic: int) -> Any | None:
        pass

