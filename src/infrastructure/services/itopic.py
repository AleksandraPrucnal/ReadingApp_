from abc import ABC, abstractmethod
from typing import Iterable, Optional

from src.core.domain.topic import Topic, TopicIn
from src.infrastructure.dto.topicDTO import TopicDTO


class ITopicService(ABC):

    @abstractmethod
    async def get_all(self) -> list[TopicDTO]:
        pass

    @abstractmethod
    async def get_by_id(self, id_topic: int) -> Optional[TopicDTO]:
        pass

    @abstractmethod
    async def create(self, data: TopicIn) -> Optional[TopicDTO]:
        pass

    @abstractmethod
    async def update(self, id_topic: int, data: TopicIn) -> Optional[TopicDTO]:
        pass

    @abstractmethod
    async def delete(self, id_topic: int) -> bool:
        pass
