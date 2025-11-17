# src/infrastructure/repositories/progress_repository.py
from datetime import datetime

from src.core.repositories.iprogress_repository import IProgressRepository
from src.db import database, progress_table
from src.core.domain.progress import ProgressIn, Progress

class ProgressRepository(IProgressRepository):
    async def add_progress(self, data: ProgressIn) -> Progress:
        query = (
            progress_table.insert()
            .values(
                user_id=data.user_id,
                exercise_id=data.exercise_id,
                rate=data.rate,
                completed_at=data.completed_at or datetime.utcnow(),
            )
            .returning(progress_table)
        )
        row = await database.fetch_one(query)
        return Progress(**dict(row))
