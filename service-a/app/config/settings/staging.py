from app.config.settings.base import BackendBaseSettings
from app.config.settings.environment import Environment


class BackendStageSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Test Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.STAGING