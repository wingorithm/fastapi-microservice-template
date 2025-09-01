import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

class BackendBaseSettings(BaseSettings):
    TITLE: str = "Service A"
    VERSION: str = "1.0.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None

    DEBUG: bool = False
    BACKEND_SERVER_HOST: str = "0.0.0.0"
    BACKEND_SERVER_PORT: int = 8081
    BACKEND_SERVER_WORKERS: int

    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # ========================= PG Database Configuration =====================
    DB_POSTGRES_HOST: str
    DB_POSTGRES_NAME: str
    DB_POSTGRES_PASSWORD: str
    DB_POSTGRES_PORT: int
    DB_POSTGRES_SCHEMA: str
    DB_POSTGRES_USERNAME: str
    IS_ALLOWED_CREDENTIALS: bool
    # ========================= PG Database Configuration =====================

    # ========================= SQLAlchemy Database Configuration =====================
    ALEMBIC_MIGRATION_ENABLE: bool
    DB_MAX_POOL_CON: int
    DB_POOL_SIZE: int
    DB_POOL_OVERFLOW: int
    DB_TIMEOUT: int

    IS_DB_ECHO_LOG: bool
    IS_DB_FORCE_ROLLBACK: bool
    IS_DB_EXPIRE_ON_COMMIT: bool
    # ========================= SQLAlchemy Database Configuration =====================

    # ========================= Client/Proxy Configuration =====================
    SERVICE_B_URL: str
    # ========================= Client/Proxy Configuration =====================

    CONFIG_SOURCE: str = "N/A"
    model_config = SettingsConfigDict(
        env_file='.env-local',
        extra="allow"
    )

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """

        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "redoc_url": self.REDOC_URL,
            "api_prefix": self.API_PREFIX,
        }