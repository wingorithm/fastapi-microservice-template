from functools import lru_cache

import decouple
from loguru import logger

from app.config.settings.base import BackendBaseSettings
from app.config.settings.development import BackendDevSettings
from app.config.settings.environment import Environment
from app.config.settings.production import BackendProdSettings
from app.config.settings.staging import BackendStageSettings


class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> BackendBaseSettings:
        if self.environment == Environment.DEVELOPMENT.value:
            return BackendDevSettings()
        elif self.environment == Environment.STAGING.value:
            return BackendStageSettings()
        return BackendProdSettings()


@lru_cache()
def get_settings() -> BackendBaseSettings:
    logger.info("CONFIGURING APP configuration...")
    return BackendSettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()


settings: BackendBaseSettings = get_settings()