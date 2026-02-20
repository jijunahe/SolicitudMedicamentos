"""
Modelo de entidad Medicamento (POS / NO POS).
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    codigo = Column(String(100), unique=True, index=True, nullable=True)
    es_pos = Column(Boolean, default=True, nullable=False)  # True = POS, False = NO POS
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    solicitudes = relationship("Solicitud", back_populates="medicamento")
