from fastapi import HTTPException, status
from uuid import UUID
from src.infrastructure.repositories.user_repository import UserRepository
from src.core.domain.user import UserIn
from src.infrastructure.dto.userDTO import UserCreate, UserDTO  # Modele API
from src.core.security import hash_password, verify_password, create_access_token
from src.core.domain.enums import UserRole as DomainUserRole


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_create: UserCreate) -> UserDTO:
        # 1. Sprawdź, czy email lub username już istnieje
        existing_user_email = await self.user_repo.get_user_by_email(user_create.email)
        if existing_user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        existing_user_username = await self.user_repo.get_user_by_username(user_create.username)
        if existing_user_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

        # 2. Zahaszuj hasło (logika biznesowa)
        hashed_pwd = hash_password(user_create.password)

        # 3. Przygotuj dane do zapisu w repozytorium
        # Tworzymy słownik zamiast obiektu UserIn, aby łatwo podmienić hasło
        user_data_for_repo = user_create.model_dump()
        user_data_for_repo["password"] = hashed_pwd
        # Konwertuj enuma z API na enuma domenowego (tutaj są identyczne, ale to dobra praktyka)
        user_data_for_repo["role"] = DomainUserRole(user_create.role.value)

        # 4. Utwórz użytkownika przez repozytorium
        created_user_domain = await self.user_repo.create_user(user_data_for_repo)

        # 5. Zwróć DTO
        return UserDTO.model_validate(created_user_domain)

    async def authenticate_user(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_user_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Tworzenie tokenu JWT
        access_token = create_access_token(
            data={"user_id": str(user.id_user), "username": user.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_user_by_id(self, user_id: UUID) -> UserDTO:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserDTO.model_validate(user)