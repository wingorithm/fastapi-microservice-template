import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command
from loguru import logger

from app.api.endpoints import router as api_endpoint_router
from app.config.events import execute_backend_server_event_handler, terminate_backend_server_event_handler
from app.config.manager import settings

def run_migrations():
    if settings.ALEMBIC_MIGRATION_ENABLE:
        logger.info("RUNNING Migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
    else:
        logger.info("SKIPPING Migrations...")

def initialize_backend_application() -> FastAPI:
    app = FastAPI(**settings.set_backend_app_attributes)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    app.include_router(router=api_endpoint_router)

    return app

backend_app: FastAPI = initialize_backend_application()
if __name__ == "__main__":
    run_migrations()
    uvicorn.run(
        app="main:backend_app",
        host=settings.BACKEND_SERVER_HOST,
        port=settings.BACKEND_SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.BACKEND_SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )