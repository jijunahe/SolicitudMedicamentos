"""
Dependencias compartidas: autenticación JWT y usuario actual.
"""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario

security = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
    db: Annotated[Session, Depends(get_db)],
) -> Usuario | None:
    """Devuelve el usuario si el token es válido; si no hay token o es inválido, None."""
    if not credentials:
        return None
    subject = decode_access_token(credentials.credentials)
    if not subject:
        return None
    user = db.query(Usuario).filter(Usuario.email == subject).first()
    return user


def get_current_user(
    current_user: Annotated[Usuario | None, Depends(get_current_user_optional)],
) -> Usuario:
    """Exige usuario autenticado; si no, 401."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado o token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
