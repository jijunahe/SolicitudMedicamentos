"""
Controlador (router) del módulo de solicitudes de medicamentos.
Crear solicitud y listar con paginación (solo autenticados).
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.usuario import Usuario
from app.schemas.solicitud import SolicitudCreate, SolicitudResponse, PaginatedSolicitudes
from app.services.solicitud_service import SolicitudService
from app.services.medicamento_service import MedicamentoService

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post("", response_model=SolicitudResponse)
def crear_solicitud(
    data: SolicitudCreate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
):
    """Crea una solicitud. Si el medicamento es NO POS, numero_orden, direccion, telefono y correo son obligatorios."""
    try:
        solicitud = SolicitudService.crear(db, current_user.id, data)
        medicamento = MedicamentoService.obtener_por_id(db, solicitud.medicamento_id)
        return SolicitudResponse(
            id=solicitud.id,
            usuario_id=solicitud.usuario_id,
            medicamento_id=solicitud.medicamento_id,
            es_no_pos=solicitud.es_no_pos,
            numero_orden=solicitud.numero_orden,
            direccion=solicitud.direccion,
            telefono=solicitud.telefono,
            correo=solicitud.correo,
            creado_en=solicitud.creado_en,
            medicamento_nombre=medicamento.nombre if medicamento else None,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=PaginatedSolicitudes)
def listar_solicitudes(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """Listado de solicitudes del usuario autenticado, con paginación."""
    return SolicitudService.listar_paginado(db, current_user.id, page=page, page_size=page_size)
