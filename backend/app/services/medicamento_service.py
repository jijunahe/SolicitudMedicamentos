"""
Servicio de medicamentos (módulo SOA).
"""
from sqlalchemy.orm import Session

from app.models.medicamento import Medicamento


class MedicamentoService:
    @staticmethod
    def listar_todos(db: Session) -> list[Medicamento]:
        return db.query(Medicamento).order_by(Medicamento.nombre).all()

    @staticmethod
    def obtener_por_id(db: Session, medicamento_id: int) -> Medicamento | None:
        return db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()
