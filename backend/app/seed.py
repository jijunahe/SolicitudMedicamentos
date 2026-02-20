"""
Semillas: datos iniciales que se cargan al arrancar si no existen.
- Medicamentos de ejemplo (POS y NO POS)
- Usuario inicial (email, password, nombre desde .env: SEED_USER_*)
"""
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal
from app.models.medicamento import Medicamento
from app.models.usuario import Usuario
from app.core.security import hash_password

MEDICAMENTOS_INICIALES = [
    {"nombre": "Acetaminofén 500mg", "codigo": "ACET500", "es_pos": True},
    {"nombre": "Ibuprofeno 400mg", "codigo": "IBU400", "es_pos": True},
    {"nombre": "Omeprazol 20mg", "codigo": "OME20", "es_pos": True},
    {"nombre": "Medicamento NO POS A", "codigo": "NOPOS-A", "es_pos": False},
    {"nombre": "Medicamento NO POS B", "codigo": "NOPOS-B", "es_pos": False},
]


def seed_medicamentos(db: Session) -> int:
    """Inserta medicamentos iniciales si la tabla está vacía. Devuelve cuántos se insertaron."""
    if db.query(Medicamento).count() > 0:
        return 0
    for m in MEDICAMENTOS_INICIALES:
        db.add(Medicamento(**m))
    db.commit()
    return len(MEDICAMENTOS_INICIALES)


def seed_usuario_inicial(db: Session) -> bool:
    """Crea el usuario inicial si no existe (email/pass/nombre desde env). Devuelve True si se creó."""
    settings = get_settings()
    email = (settings.SEED_USER_EMAIL or "").strip()
    if not email:
        return False
    if db.query(Usuario).filter(Usuario.email == email).first():
        return False
    db.add(
        Usuario(
            email=email,
            password_hash=hash_password(settings.SEED_USER_PASSWORD),
            nombre=settings.SEED_USER_NOMBRE or None,
        )
    )
    db.commit()
    return True


def run_seed():
    """Ejecuta todas las semillas. Idempotente: no duplica datos."""
    db = SessionLocal()
    try:
        n_med = seed_medicamentos(db)
        created_user = seed_usuario_inicial(db)
        if n_med or created_user:
            msg = []
            if n_med:
                msg.append(f"{n_med} medicamentos iniciales")
            if created_user:
                msg.append(f"usuario {get_settings().SEED_USER_EMAIL}")
            print(f"[seed] Cargados: {', '.join(msg)}")
    finally:
        db.close()
