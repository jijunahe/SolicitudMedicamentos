"""
Servicio de autenticación (módulo SOA).
"""
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.auth import UserCreate, UserResponse
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    @staticmethod
    def register(db: Session, data: UserCreate) -> Usuario:
        if db.query(Usuario).filter(Usuario.email == data.email).first():
            raise ValueError("El email ya está registrado")
        user = Usuario(
            email=data.email,
            password_hash=hash_password(data.password),
            nombre=data.nombre,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> tuple[Usuario, str]:
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Credenciales inválidas")
        token = create_access_token(subject=user.email)
        return user, token
