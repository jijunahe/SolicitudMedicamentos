#!/usr/bin/env python3
"""
Crea el usuario nevaEps en la tabla usuarios con la contraseña hasheada
con el mismo algoritmo (bcrypt) que usa el backend.
Ejecutar desde backend: cd backend && python3 scripts/crear_usuario_nevaeps.py
"""
import sys
import os

# Asegurar que app se importe desde backend
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.security import hash_password
from app.database import SessionLocal
from app.models.usuario import Usuario

EMAIL = "nevaEps@eps.local"
PASSWORD_PLAIN = "12345678"
NOMBRE = "nevaEps"


def main():
    password_hash = hash_password(PASSWORD_PLAIN)
    db = SessionLocal()
    try:
        existing = db.query(Usuario).filter(Usuario.email == EMAIL).first()
        if existing:
            print(f"El usuario {EMAIL} ya existe. Actualizando contraseña...")
            existing.password_hash = password_hash
            existing.nombre = NOMBRE
            db.commit()
            print("Contraseña actualizada.")
        else:
            user = Usuario(
                email=EMAIL,
                password_hash=password_hash,
                nombre=NOMBRE,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Usuario creado: {EMAIL} (nombre: {NOMBRE})")
        print("Puedes iniciar sesión en la app con:")
        print(f"  Email:    {EMAIL}")
        print(f"  Password: {PASSWORD_PLAIN}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
