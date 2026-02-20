"""
Esquemas Pydantic para autenticación.
"""
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nombre: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    nombre: str | None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
