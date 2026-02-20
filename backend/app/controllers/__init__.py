from app.controllers.auth_controller import router as auth_router
from app.controllers.medicamentos_controller import router as medicamentos_router
from app.controllers.solicitudes_controller import router as solicitudes_router

__all__ = ["auth_router", "medicamentos_router", "solicitudes_router"]
