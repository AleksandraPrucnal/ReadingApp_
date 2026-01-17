from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, delete

from src.core.domain.preferences import Preferences
from src.core.repositories.ipreferences_repository import IPreferencesRepository
from src.db import (
    database,
    preferences_table,
    preferences_topics_table,
)

class PreferencesRepository(IPreferencesRepository):

    async def get_by_user_id(self, user_id: UUID) -> Optional[Preferences]:
        query = select(preferences_table).where(preferences_table.c.user_id == user_id)
        row = await database.fetch_one(query)

        if not row:
            return None

        topics_query = select(preferences_topics_table.c.topic_id).where(
            preferences_topics_table.c.user_id == user_id
        )
        topics_rows = await database.fetch_all(topics_query)
        topic_ids = [r["topic_id"] for r in topics_rows]

        return Preferences(
            id_user=row["user_id"],
            topics=topic_ids,
            favourite_names=row["favourite_names"],
            family_names=row["family_names"],
            ui_mode=row["ui_mode"],
            level=row["level"]
        )

    async def set_preferences(self, user_id: UUID, data: Preferences) -> Preferences:
        async with database.transaction():
            # 1. Sprawdź, czy rekord już istnieje
            check_query = select(preferences_table.c.user_id).where(
                preferences_table.c.user_id == user_id
            )
            exists = await database.fetch_one(check_query)

            # 2. Insert lub Update tabeli głównej
            values = {
                "favourite_names": data.favourite_names,
                "family_names": data.family_names,
                "ui_mode": data.ui_mode.value,
                "level": data.level
            }

            if exists:
                await database.execute(
                    preferences_table.update()
                    .where(preferences_table.c.user_id == user_id)
                    .values(**values)
                )
            else:
                values["user_id"] = user_id
                await database.execute(preferences_table.insert().values(**values))

            # 3. Obsługa tematów (Many-to-Many)
            await database.execute(
                preferences_topics_table.delete().where(
                    preferences_topics_table.c.user_id == user_id
                )
            )

            if data.topics:
                topics_values = [
                    {"user_id": user_id, "topic_id": tid}
                    for tid in data.topics
                ]
                await database.execute(
                    preferences_topics_table.insert().values(topics_values)
                )

        # 4. Zwróć zaktualizowany obiekt (ponownie pobierając go z bazy dla pewności)
        saved = await self.get_by_user_id(user_id)
        if not saved:
            raise RuntimeError("Critical error: Preferences saved but not found.")
        return saved