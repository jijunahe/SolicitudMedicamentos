"""
Punto de entrada FastAPI. Registro de routers y documentación Swagger.
"""
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import engine, Base
from app.controllers import auth_router, medicamentos_router, solicitudes_router


def _wait_for_db(max_attempts: int = 30, interval: float = 2.0) -> None:
    """Espera a que MySQL acepte conexiones (útil en Docker)."""
    for attempt in range(max_attempts):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return
        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"No se pudo conectar a la BD después de {max_attempts} intentos: {e}") from e
            time.sleep(interval)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crear tablas y cargar semillas al arranque (en producción usar migraciones)."""
    _wait_for_db()
    Base.metadata.create_all(bind=engine)
    from app.seed import run_seed
    run_seed()
    yield
    # shutdown si hiciera falta
    pass


app = FastAPI(
    title="API Solicitud de Medicamentos",
    description="API REST para autenticación y gestión de solicitudes de medicamentos (POS/NO POS).",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(medicamentos_router)
app.include_router(solicitudes_router)


@app.get("/health")
def health():
    return {"status": "ok"}
