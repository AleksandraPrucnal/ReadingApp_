from src.infrastructure.repositories.progress_repository import ProgressRepository
from src.core.domain.progress import ProgressIn, Progress

class ProgressService:
    def __init__(self, repository: ProgressRepository):
        self._repository = repository

    async def save_progress(self, data: ProgressIn) -> Progress:
        return await self._repository.add_progress(data)
