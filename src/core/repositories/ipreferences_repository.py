from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from src.core.domain.preferences import Preferences

class IPreferencesRepository(ABC):

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Preferences]:
        """
        Pobiera preferencje użytkownika na podstawie jego UUID.
        Zwraca obiekt domeny Preferences lub None, jeśli użytkownik nie ma jeszcze ustawień.
        """
        pass

    @abstractmethod
    async def set_preferences(self, user_id: UUID, data: Preferences) -> Preferences:
        """
        Tworzy lub aktualizuje preferencje użytkownika (UPSERT).
        Nadpisuje listę tematów, imiona ulubione oraz imiona w rodzinie.
        Zwraca zaktualizowany obiekt Preferences.
        """
        pass