from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from uuid import UUID

from src.infrastructure.dto.userDTO import UserCreate, UserDTO, Token
from src.infrastructure.services.user import UserService
from src.api.dependencies import get_user_service, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication & Users"])

@router.post("/register", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """
    Rejestruje nowego użytkownika.
    """
    return await user_service.register_user(user_in)

@router.post("/authenticate", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service)
):
    """
    Loguje użytkownika i zwraca token JWT.
    **Ważne:** Używa `application/x-www-form-urlencoded` (standard OAuth2).
    'username' w formularzu to email użytkownika.
    """
    # Używamy form_data.username jako email
    token = await user_service.authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    return token

@router.get("/me", response_model=UserDTO)
async def read_users_me(
    current_user: UserDTO = Depends(get_current_user)
):
    """
    Zwraca dane aktualnie zalogowanego użytkownika.
    """
    return current_user

@router.get("/users/{user_id}", response_model=UserDTO)
async def read_user_by_id(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    current_user: UserDTO = Depends(get_current_user) # Zabezpieczenie endpointu
):
    """
    Pobiera dane użytkownika po ID.
    (Obecnie wymaga bycia zalogowanym, aby zobaczyć kogokolwiek).
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user