import typing

import loguru
from fastapi import FastAPI

from app.repository.events import dispose_db_connection, initialize_db_connection
from app.config.manager import settings

def execute_backend_server_event_handler(backend_app: FastAPI) -> typing.Any:
    async def launch_backend_server_events() -> None:
        await initialize_db_connection(backend_app=backend_app)
        # add other DB if needed
    loguru.logger.info(f"FASTAPI BACKEND SERVER RUNNING ON {settings.BACKEND_SERVER_HOST}:{settings.BACKEND_SERVER_PORT}")
    return launch_backend_server_events


def terminate_backend_server_event_handler(backend_app: FastAPI) -> typing.Any:
    @loguru.logger.catch
    async def stop_backend_server_events() -> None:
        await dispose_db_connection(backend_app=backend_app)
        # add other DB if needed

    return stop_backend_server_events
