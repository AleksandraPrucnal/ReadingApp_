from typing import Iterable, Optional, List

from src.core.domain.topic import Topic, TopicIn
from src.db import database, topic_table
from sqlalchemy import select
from src.core.repositories.itopic_repository import ITopicRepository


class TopicRepository(ITopicRepository):

    async def get_all(self) -> Iterable[Topic]:
        query = topic_table.select().order_by(topic_table.c.name.asc())
        rows = await database.fetch_all(query)
        return [Topic(**dict(row)) for row in rows]

    async def get_by_id(self, id_topic: int) -> Optional[Topic]:
        row = await database.fetch_one(
            select(topic_table).where(topic_table.c.id_topic == id_topic) #ignore: type
        )
        return Topic(**dict(row)) if row else None

    async def get_by_name(self, name: str) -> Optional[Topic]:
        row = await database.fetch_one(
            select(topic_table).where(topic_table.c.name == name) #ignore: type
        )
        return Topic(**dict(row)) if row else None


    async def add(self, data: TopicIn) -> Optional[Topic]:
        new_id = await database.execute(
            topic_table.insert().values(name=data.name)
        )
        return await self.get_by_id(new_id)

    async def update(self, id_topic: int, data: TopicIn) -> Optional[Topic]:
        exists = await self.get_by_id(id_topic)
        if not exists:
            return None

        await database.execute(
            topic_table.update()
            .where(topic_table.c.id_topic == id_topic)
            .values(name=data.name)
        )
        return await self.get_by_id(id_topic)

    async def delete(self, id_topic: int) -> bool:
        exists = await self.get_by_id(id_topic)
        if not exists:
            return False

        await database.execute(
            topic_table.delete().where(topic_table.c.id_topic == id_topic)
        )
        return True
