"""
Esquemas Pydantic para medicamentos.
"""
from pydantic import BaseModel


class MedicamentoResponse(BaseModel):
    id: int
    nombre: str
    codigo: str | None
    es_pos: bool

    class Config:
        from_attributes = True


class MedicamentoList(BaseModel):
    items: list[MedicamentoResponse]
