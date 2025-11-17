from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from uuid import UUID

# Twój UserRole enum (używany w DTO)
class UserRole(str, Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    MANAGER = "manager"

# Twój UserDTO (do zwracania danych usera)
class UserDTO(BaseModel):
    id_user: UUID
    username: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

# Model do tworzenia usera (przyjmowany przez endpoint /register)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.STUDENT

# Model do odpowiedzi tokenu
class Token(BaseModel):
    access_token: str
    token_type: str

# Model danych wewnątrz tokenu
class TokenData(BaseModel):
    username: str | None = None
    user_id: str | None = None