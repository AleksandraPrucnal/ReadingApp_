from sqlalchemy import select, desc
from uuid import UUID
from typing import Iterable

from src.db import database
from src.db import progress_table
from src.core.domain.progress import ProgressIn


class ProgressRepository:

    async def add_progress(self, data: ProgressIn) -> None:
        values = data.model_dump()

        if 'id_exercise' in values:
            values['exercise_id'] = values.pop('id_exercise')

        query = progress_table.insert().values(**values)
        await database.execute(query)

    async def get_user_history(self, user_id: UUID) -> Iterable[dict]:
        """
        Pobiera historię punktów dla danego użytkownika.
        """
        query = (
            select(
                progress_table.c.rate,
                progress_table.c.completed_at
            )
            .where(progress_table.c.user_id == user_id)
            .order_by(desc(progress_table.c.completed_at))
        )

        rows = await database.fetch_all(query)
        return [dict(row) for row in rows]