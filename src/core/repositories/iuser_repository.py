from abc import ABC, abstractmethod
from typing import Optional, Any
from uuid import UUID

from src.core.domain.user import UserIn


class IUserRepository(ABC):

    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """Register a new user."""
        pass

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID) -> Any | None:
        """Get user by UUID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """Get user by email."""
        pass