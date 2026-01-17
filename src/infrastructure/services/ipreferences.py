from abc import ABC, abstractmethod
from uuid import UUID

from src.infrastructure.dto.preferencesDTO import PreferencesDTO


class IPreferencesService(ABC):

    @abstractmethod
    async def get_user_preferences(self, user_id: UUID) -> PreferencesDTO:
        """
        Pobiera preferencje dla danego użytkownika.
        Jeśli użytkownik nie ma preferencji, powinien zwrócić domyślny obiekt DTO.
        """
        pass

    @abstractmethod
    async def set_user_preferences(self, user_id: UUID, data: PreferencesDTO) -> PreferencesDTO:
        """
        Zapisuje lub aktualizuje preferencje użytkownika.
        """
        pass