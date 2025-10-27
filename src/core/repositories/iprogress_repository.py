# src/infrastructure/repositories/progress_repository.py
from abc import ABC
from datetime import datetime
from typing import Any

from src.db import database, progress_table
from src.core.domain.progress import ProgressIn, Progress

class IProgressRepository(ABC):
    async def add_progress(self, data: ProgressIn) -> Any | None:
        pass
