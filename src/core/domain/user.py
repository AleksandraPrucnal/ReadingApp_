from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from src.core.domain.enums import UserRole
from src.core.domain.preferences import Preferences

class UserIn(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.STUDENT

class User(UserIn):
    id_user: UUID
    model_config = ConfigDict(from_attributes=True, extra="ignore")