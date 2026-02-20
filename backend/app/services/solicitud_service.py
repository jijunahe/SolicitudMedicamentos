"""
Servicio de solicitudes de medicamentos (módulo SOA).
Validaciones: si medicamento es NO POS, numero_orden, direccion, telefono y correo obligatorios.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.solicitud import Solicitud
from app.models.medicamento import Medicamento
from app.schemas.solicitud import SolicitudCreate, PaginatedSolicitudes, SolicitudListResponse


class SolicitudService:
    @staticmethod
    def crear(
        db: Session,
        usuario_id: int,
        data: SolicitudCreate,
    ) -> Solicitud:
        medicamento = db.query(Medicamento).filter(Medicamento.id == data.medicamento_id).first()
        if not medicamento:
            raise ValueError("Medicamento no encontrado")

        es_no_pos = not medicamento.es_pos
        if es_no_pos:
            if not all([data.numero_orden, data.direccion, data.telefono, data.correo]):
                raise ValueError(
                    "Para medicamentos NO POS son obligatorios: número de orden, dirección, teléfono y correo."
                )

        solicitud = Solicitud(
            usuario_id=usuario_id,
            medicamento_id=data.medicamento_id,
            es_no_pos=es_no_pos,
            numero_orden=data.numero_orden if es_no_pos else None,
            direccion=data.direccion if es_no_pos else None,
            telefono=data.telefono if es_no_pos else None,
            correo=data.correo if es_no_pos else None,
        )
        db.add(solicitud)
        db.commit()
        db.refresh(solicitud)
        return solicitud

    @staticmethod
    def listar_paginado(
        db: Session,
        usuario_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> PaginatedSolicitudes:
        query = (
            db.query(Solicitud, Medicamento.nombre.label("medicamento_nombre"))
            .join(Medicamento, Solicitud.medicamento_id == Medicamento.id)
            .filter(Solicitud.usuario_id == usuario_id)
            .order_by(desc(Solicitud.creado_en))
        )
        total = query.count()
        offset = (page - 1) * page_size
        rows = query.offset(offset).limit(page_size).all()

        items = [
            SolicitudListResponse(
                id=s.id,
                medicamento_nombre=med_nombre,
                es_no_pos=s.es_no_pos,
                creado_en=s.creado_en,
            )
            for s, med_nombre in rows
        ]
        pages = (total + page_size - 1) // page_size if page_size else 0
        return PaginatedSolicitudes(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )
