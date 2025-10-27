from datetime import datetime, timedelta, timezone

from jose import jwt
from pydantic import UUID4

from src.infrastructure.utils.consts import (
    EXPIRATION_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)


def generate_user_token(user_uuid: UUID4, role: str) -> dict:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_MINUTES)
    jwt_data = {
        "sub": str(user_uuid),
        "role": role,               # <--- rola użytkownika
        "exp": expire,
        "type": "access"
    }
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": encoded_jwt, "expires": expire}
