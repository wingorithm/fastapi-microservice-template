from app.config.settings.base import BackendBaseSettings
from app.config.settings.environment import Environment

class BackendProdSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Production Environment."
    ENVIRONMENT: Environment = Environment.PRODUCTION