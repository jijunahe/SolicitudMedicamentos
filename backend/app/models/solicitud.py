"""
Modelo de entidad Solicitud de medicamento.
Campos adicionales obligatorios cuando el medicamento es NO POS.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"), nullable=False)

    # Para NO POS (obligatorios en ese caso)
    es_no_pos = Column(Boolean, default=False, nullable=False)
    numero_orden = Column(String(255), nullable=True)
    direccion = Column(Text, nullable=True)
    telefono = Column(String(50), nullable=True)
    correo = Column(String(255), nullable=True)

    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="solicitudes")
    medicamento = relationship("Medicamento", back_populates="solicitudes")
