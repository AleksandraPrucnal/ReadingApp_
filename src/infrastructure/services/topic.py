from typing import Iterable, Optional

from src.core.domain.topic import Topic, TopicIn
from src.core.repositories.itopic_repository import ITopicRepository
from src.infrastructure.dto.topicDTO import TopicDTO
from src.infrastructure.services.itopic import ITopicService


class TopicService(ITopicService):
    def __init__(self, repository: ITopicRepository) -> None:
        self._repository = repository

    async def get_all(self) -> list[TopicDTO]:
        rows: Iterable[Topic] = await self._repository.get_all()
        return [TopicDTO(**t.__dict__) if not isinstance(t, dict) else TopicDTO(**t) for t in rows]

    async def get_by_id(self, id_topic: int) -> Optional[TopicDTO]:
        row = await self._repository.get_by_id(id_topic)
        if not row:
            return None
        return TopicDTO(**row.__dict__) if not isinstance(row, dict) else TopicDTO(**row)

    async def create(self, data: TopicIn) -> Optional[TopicDTO]:
        exists = await self._repository.get_by_name(data.name)
        if exists:
            return None
        row = await self._repository.add(data)
        if not row:
            return None
        return TopicDTO(**row.__dict__) if not isinstance(row, dict) else TopicDTO(**row)

    async def update(self, id_topic: int, data: TopicIn) -> Optional[TopicDTO]:
        other = await self._repository.get_by_name(data.name)
        if other and getattr(other, "id_topic", None) != id_topic:
            return None

        row = await self._repository.update(id_topic, data)
        if not row:
            return None
        return TopicDTO(**row.__dict__) if not isinstance(row, dict) else TopicDTO(**row)

    async def delete(self, id_topic: int) -> bool:
        return await self._repository.delete(id_topic)
