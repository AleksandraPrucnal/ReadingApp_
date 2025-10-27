from uuid import UUID

from src.core.domain.user import UserIn
from src.core.repositories.iuser_repository import IUserRepository
from src.infrastructure.dto.userDTO import UserDTO
from src.infrastructure.dto.tokenDTO import TokenDTO
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.utils.password import verify_password
from src.infrastructure.utils.token import generate_user_token


class UserService(IUserService):
    """An abstract class for user service."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def register_user(self, user: UserIn) -> UserDTO | None:

        return await self._repository.register_user(user)

    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating the user."""

        if user_data := await self._repository.get_by_email(user.email):
            if verify_password(user.password, user_data.password):
                token_details = generate_user_token(
                    user_data.id_user,
                    user_data.role.value if hasattr(user_data.role, "value") else user_data.role
                )
                return TokenDTO(token_type="Bearer", **token_details)
            return None

        return None

    async def get_by_uuid(self, uuid: UUID) -> UserDTO | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID5): The UUID of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self._repository.get_by_uuid(uuid)

    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self.get_by_email(email)