from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import noload
from uuid import UUID
from src.db import user_table
from src.core.domain.user import User
from src.core.security import hash_password

from src.db import database  # <-- Importuje obiekt 'database'




class UserRepository:
    # Nie ma __init__ z sesją, bo używamy globalnego 'database'

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """
        Pobiera użytkownika po jego UUID.
        Używane przez /auth/me.
        """
        # Ta funkcja była prawdopodobnie błędna
        query = user_table.select().where(user_table.c.id_user == user_id)
        row = await database.fetch_one(query)
        return User(**row) if row else None

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Pobiera użytkownika po jego adresie email.
        Używane przez /auth/authenticate.
        """
        # Ta funkcja była poprawna
        query = user_table.select().where(user_table.c.email == email)
        row = await database.fetch_one(query)
        return User(**row) if row else None

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Pobiera użytkownika po jego nazwie.
        Używane przy rejestracji do sprawdzania duplikatów.
        """
        query = user_table.select().where(user_table.c.username == username)
        row = await database.fetch_one(query)
        return User(**row) if row else None

    async def create_user(self, user_data: dict) -> User:
        """
        Tworzy nowego użytkownika.
        Używane przez /auth/register.
        """
        query = user_table.insert().values(**user_data).returning(user_table)
        created_user_row = await database.fetch_one(query)

        if created_user_row is None:
            raise Exception("Nie udało się utworzyć użytkownika")  # Zabezpieczenie

        return User(**created_user_row)

class UserRepository:
    # Nie ma __init__ z sesją

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = user_table.select().where(user_table.c.id_user == user_id)
        row = await database.fetch_one(query)  # Używa database.fetch_one
        return User(**row) if row else None

    async def get_user_by_email(self, email: str) -> User | None:
        query = user_table.select().where(user_table.c.email == email)
        row = await database.fetch_one(query)
        return User(**row) if row else None

    async def get_user_by_username(self, username: str) -> User | None:
        query = user_table.select().where(user_table.c.username == username)
        row = await database.fetch_one(query)
        return User(**row) if row else None

    async def create_user(self, user_data: dict) -> User:
        query = user_table.insert().values(**user_data).returning(user_table)
        created_user_row = await database.fetch_one(query)
        return User(**created_user_row)