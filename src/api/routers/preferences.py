"""Preferences endpoints."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.container import Container
from src.infrastructure.dto.preferencesDTO import PreferencesDTO
from src.infrastructure.services.ipreferences import IPreferencesService
from src.api.dependencies import get_current_user, CurrentUser

# Router nie ma prefixu "/exercises", bo endpointy brzmią "/user/preferences"
router = APIRouter(tags=["preferences"])


@router.get("/user/preferences", response_model=PreferencesDTO, status_code=200)
@inject
async def get_my_preferences(
        service: IPreferencesService = Depends(Provide[Container.preferences_service]),
        user: CurrentUser = Depends(get_current_user),
) -> PreferencesDTO:
    """
    Pobiera preferencje (imiona, motyw, poziom) zalogowanego użytkownika.
    Jeśli użytkownik nie ma jeszcze ustawień, zwraca domyślny obiekt.
    """
    return await service.get_user_preferences(user.id_user)


@router.post("/user/preferences", response_model=PreferencesDTO, status_code=200)
@inject
async def update_my_preferences(
        body: PreferencesDTO,
        service: IPreferencesService = Depends(Provide[Container.preferences_service]),
        user: CurrentUser = Depends(get_current_user),
) -> PreferencesDTO:
    """
    Tworzy lub aktualizuje preferencje zalogowanego użytkownika.
    Nadpisuje ID użytkownika w body ID pobranym z tokena (dla bezpieczeństwa).
    """
    # Zabezpieczenie: wymuszamy ID zalogowanego użytkownika,
    # niezależnie od tego co ktoś przysłał w JSON.
    body.id_user = user.id_user

    return await service.set_user_preferences(user.id_user, body)