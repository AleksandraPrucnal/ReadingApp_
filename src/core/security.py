from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

# === KLUCZOWA POPRAWKA ===
# Importujemy 'settings' z Twojego pliku Pydantic (na podstawie logów)
# a nie z ogólnego 'src.config'
from src.core.config_user import settings

# Kontekst hashowania
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Sprawdza, czy hasło pasuje do hasha."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Hashuje hasło."""
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """Tworzy nowy token JWT."""
    to_encode = data.copy()

    # Wczytujemy ustawienia (teraz na pewno istnieją dzięki docker-compose)
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """Dekoduje token JWT i zwraca jego zawartość (payload)."""
    try:
        # Upewniamy się, że algorytmy są listą (ważne dla `jose`)
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        # Zostawiamy log, aby widzieć błędy, jeśli nadal wystąpią
        print(f"--- [SECURITY ERROR] Błąd dekodowania tokenu: {e} ---")
        return None