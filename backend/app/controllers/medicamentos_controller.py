"""
Controlador (router) del módulo de medicamentos.
Listado de medicamentos (para selector en formulario de solicitud).
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medicamento import MedicamentoResponse, MedicamentoList
from app.services.medicamento_service import MedicamentoService

router = APIRouter(prefix="/medicamentos", tags=["Medicamentos"])


@router.get("", response_model=MedicamentoList)
def listar_medicamentos(
    db: Annotated[Session, Depends(get_db)],
):
    """Listado de todos los medicamentos (POS y NO POS) para el formulario."""
    items = MedicamentoService.listar_todos(db)
    return MedicamentoList(items=[MedicamentoResponse.model_validate(m) for m in items])
