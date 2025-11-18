from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.infrastructure.services.progress import ProgressService
from src.infrastructure.dto.progressDTO import UserProgressDTO

from src.api.dependencies import get_current_user, CurrentUser

router = APIRouter(tags=["progress"])

@router.get("/me", response_model=UserProgressDTO)
@inject
async def my_progress(
    service: ProgressService = Depends(Provide[Container.progress_service]),
    user: CurrentUser = Depends(get_current_user)
):
    """
    Pobiera statystyki levelu i historię punktów dla wykresu.
    Wymaga zalogowania.
    """
    return await service.get_user_stats(user.id_user)