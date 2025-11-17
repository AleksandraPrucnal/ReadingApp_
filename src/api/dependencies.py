from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.security import decode_access_token
from src.infrastructure.dto.userDTO import UserDTO
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/authenticate")
CurrentUser = UserDTO


# --- TE FUNKCJE SĄ POTRZEBNE DO ROUTERA USER.PY ---
def get_user_repository() -> UserRepository:
    return UserRepository()


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


# -------------------------------------------------

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDTO:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",  # To jest komunikat, który widzisz na ekranie telefonu
        headers={"WWW-Authenticate": "Bearer"},
    )

    print(f"\n--- [AUTH START] Token: {token[:10]}... ---")

    # 1. Dekodowanie (Tu używamy klucza "NA SZTYWNO" z security.py)
    payload = decode_access_token(token)

    if payload is None:
        print("--- [AUTH FAIL] decode_access_token zwrócił None (Błąd podpisu/klucza) ---")
        raise credentials_exception

    user_id_str: str | None = payload.get("user_id")
    if user_id_str is None:
        print("--- [AUTH FAIL] Brak user_id w payloadzie ---")
        raise credentials_exception

    # 2. Baza Danych
    try:
        user_id = UUID(user_id_str)
        user_repo = UserRepository()
        user = await user_repo.get_user_by_id(user_id)

        if user is None:
            print(f"--- [AUTH FAIL] User {user_id} nie istnieje w bazie ---")
            raise credentials_exception

        print(f"--- [AUTH SUCCESS] Zalogowano: {user.username} ---")
        return UserDTO.model_validate(user)

    except Exception as e:
        print(f"--- [AUTH ERROR] Wyjątek: {e} ---")
        raise credentials_exception