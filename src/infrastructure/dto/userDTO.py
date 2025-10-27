from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    MANAGER = "manager"

class UserDTO(BaseModel):
    id_user: UUID
    username: str
    email: EmailStr
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )