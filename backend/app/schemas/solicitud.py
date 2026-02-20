"""
Esquemas Pydantic para solicitudes.
Validaciones: campos obligatorios para NO POS.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class SolicitudCreateNoPos(BaseModel):
    """Campos adicionales obligatorios cuando el medicamento es NO POS."""
    numero_orden: str = Field(..., min_length=1)
    direccion: str = Field(..., min_length=1)
    telefono: str = Field(..., min_length=1)
    correo: EmailStr


class SolicitudCreate(BaseModel):
    medicamento_id: int
    # Opcionales; si el medicamento es NO POS deben enviarse y validarse en servicio
    numero_orden: str | None = None
    direccion: str | None = None
    telefono: str | None = None
    correo: EmailStr | None = None


class SolicitudResponse(BaseModel):
    id: int
    usuario_id: int
    medicamento_id: int
    es_no_pos: bool
    numero_orden: str | None
    direccion: str | None
    telefono: str | None
    correo: str | None
    creado_en: datetime
    medicamento_nombre: str | None = None

    class Config:
        from_attributes = True


class SolicitudListResponse(BaseModel):
    id: int
    medicamento_nombre: str
    es_no_pos: bool
    creado_en: datetime

    class Config:
        from_attributes = True


class PaginatedSolicitudes(BaseModel):
    items: list[SolicitudListResponse]
    total: int
    page: int
    page_size: int
    pages: int
