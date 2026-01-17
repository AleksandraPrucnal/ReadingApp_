from uuid import UUID

from src.core.domain.preferences import Preferences
from src.core.domain.enums import UiMode
from src.core.repositories.ipreferences_repository import IPreferencesRepository
from src.infrastructure.services.ipreferences import IPreferencesService
from src.infrastructure.dto.preferencesDTO import PreferencesDTO


class PreferencesService(IPreferencesService):
    """
    Serwis odpowiedzialny za logikę biznesową preferencji.
    Deleguje operacje CRUD do repozytorium, ale operuje na DTO dla warstwy API.
    """

    _repository: IPreferencesRepository

    def __init__(self, repository: IPreferencesRepository) -> None:
        self._repository = repository

    async def get_user_preferences(self, user_id: UUID) -> PreferencesDTO:
        # 1. Pobierz domenowy obiekt z repozytorium
        domain_obj = await self._repository.get_by_user_id(user_id)

        # 2. Jeśli nie istnieje, zwróć domyślny DTO (pusty)
        # Dzięki temu frontend zawsze dostanie poprawny JSON, nawet przy pierwszym logowaniu
        if not domain_obj:
            return PreferencesDTO(
                id_user=user_id,
                topics=[],
                favourite_names=[],
                family_names={},
                ui_mode=UiMode.LIGHT, # Domyślna wartość
                level=1
            )

        # 3. Konwersja Model Domeny -> DTO
        return PreferencesDTO.model_validate(domain_obj)

    async def set_user_preferences(self, user_id: UUID, data: PreferencesDTO) -> PreferencesDTO:
        # 1. Konwersja DTO -> Model Domeny
        # Ważne: Nadpisujemy id_user tym z tokena (user_id), dla bezpieczeństwa
        domain_in = Preferences(
            id_user=user_id,
            topics=data.topics,
            favourite_names=data.favourite_names,
            family_names=data.family_names,
            ui_mode=data.ui_mode,
            level=data.level
        )

        # 2. Zapis w repozytorium
        saved_domain = await self._repository.set_preferences(user_id, domain_in)

        # 3. Konwersja powrotna Model Domeny -> DTO
        return PreferencesDTO.model_validate(saved_domain)