"""
Controlador (router) del módulo de autenticación.
Endpoints: /auth/register, /auth/login
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserCreate, UserResponse, Token, LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UserResponse)
def register(
    data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    """Registro de nuevo usuario. Password almacenado encriptado."""
    try:
        user = AuthService.register(db, data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
def login(
    data: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Login: devuelve JWT access_token."""
    try:
        _, token = AuthService.login(db, data.email, data.password)
        return Token(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
