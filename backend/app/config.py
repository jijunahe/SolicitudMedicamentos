"""
Configuración de la aplicación desde variables de entorno.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración cargada desde .env."""

    # Base de datos MySQL
    DB_USER: str = "eps"
    DB_PASSWORD: str = "12345678"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "solicitud_medicamentos"

    # JWT
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

    # Usuario inicial (semilla)
    SEED_USER_EMAIL: str = "nevaEps@eps.local"
    SEED_USER_PASSWORD: str = "12345678"
    SEED_USER_NOMBRE: str = "nevaEps"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
