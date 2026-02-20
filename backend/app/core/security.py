"""
Seguridad: hashing de contraseñas (bcrypt) y JWT.
"""
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt

from app.config import get_settings

settings = get_settings()

# bcrypt tiene límite de 72 bytes
MAX_BCRYPT_BYTES = 72


def _to_bytes(password: str) -> bytes:
    """Convierte la contraseña a bytes y trunca a 72 bytes (límite de bcrypt)."""
    raw = password.encode("utf-8")
    if len(raw) > MAX_BCRYPT_BYTES:
        raw = raw[:MAX_BCRYPT_BYTES]
    return raw


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(_to_bytes(plain), hashed.encode("utf-8"))
    except Exception:
        return False


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload.get("sub")
    except jwt.PyJWTError:
        return None
