from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from uuid import UUID

from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.services.user import UserService
from src.core.security import decode_access_token
from src.infrastructure.dto.userDTO import TokenData, UserDTO


from src.core.security import decode_access_token
from src.infrastructure.dto.userDTO import TokenData, UserDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/authenticate")


def get_user_repository() -> UserRepository:
    """Zależność zwracająca instancję UserRepository."""
    return UserRepository()


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    """Zależność zwracająca instancję UserService."""
    return UserService(repo)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(get_user_service)
) -> UserDTO:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id_str = payload.get("user_id")
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise credentials_exception

    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user