from typing import Any
from uuid import UUID
from src.infrastructure.utils.password import hash_password
from src.core.domain.user import UserIn
from src.core.repositories.iuser_repository import IUserRepository
from src.db import database, user_table
from sqlalchemy import insert
import asyncpg


class UserRepository(IUserRepository):

    async def register_user(self, user: UserIn) -> Any | None:
        hashed = hash_password(user.password)
        payload = user.model_dump(mode="json")
        payload["password"] = hashed

        stmt = (
            insert(user_table)
            .values(**payload)
            .returning(user_table.c.id_user)
        )

        async with database.transaction():
            existing = await database.fetch_one(
                user_table.select().where(user_table.c.email == user.email)
            )
            if existing:
                return None

            try:
                new_user_uuid = await database.execute(stmt)
            except asyncpg.UniqueViolationError:
                return None

            return await database.fetch_one(
                user_table.select().where(user_table.c.id_user == new_user_uuid)
            )

    async def get_by_uuid(self, uuid: UUID) -> Any | None:

        query = user_table \
            .select() \
            .where(user_table.c.id_user == uuid)
        user = await database.fetch_one(query)

        return user

    async def get_by_email(self, email: str) -> Any | None:

        query = user_table \
            .select() \
            .where(user_table.c.email == email)
        user = await database.fetch_one(query)

        return user