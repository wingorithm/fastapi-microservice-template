import os
from loguru import logger
from functools import lru_cache
import consul

from app.config.settings.base import BackendBaseSettings
from app.config.settings.development import BackendDevSettings
from app.config.settings.environment import Environment
from app.config.settings.production import BackendProdSettings
from app.config.settings.staging import BackendStageSettings

CONSUL_HOST = os.getenv("CONSUL_HOST", "localhost")
CONSUL_PORT = int(os.getenv("CONSUL_PORT", 8500))
SERVICE_NAME = os.getenv("SERVICE_NAME", "service-b")
CONSUL_KV_PATH_PREFIX = f"config/{SERVICE_NAME}/"

def _fetch_config_from_consul() -> dict[str, str | int | bool]:
    """
        Attempts to connect to Consul and fetch all K/V pairs for the service.
        Returns a dictionary of configuration values if successful, otherwise empty.
        """
    try:
        c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
        index, data = c.kv.get(CONSUL_KV_PATH_PREFIX, recurse=True)
        if data is None:
            logger.warning(f"No config found in Consul at prefix: '{CONSUL_KV_PATH_PREFIX}'")
            return {}
        config_dict = {}
        for item in data:
            key = item['Key'].replace(CONSUL_KV_PATH_PREFIX, '')
            if not key:
                continue
            if item['Value'] is not None:
                value = item['Value'].decode('utf-8-sig').strip()
                config_dict[key] = value
        logger.info(f"Successfully loaded {len(config_dict)} keys from Consul.")
        return config_dict
    except Exception as e:
        logger.warning(f"Could not connect to Consul or fetch config: {e}")
        logger.warning("Consul is unavailable. Will attempt to use fallback.")
        return {}

class BackendSettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self, config_data: dict | None = None) -> BackendBaseSettings:
        """
        Instantiates the correct settings class based on the environment
        and populates it with data from the provided source.
        """
        settings_classes = {
            Environment.DEVELOPMENT.value: BackendDevSettings,
            Environment.STAGING.value: BackendStageSettings,
            Environment.PRODUCTION.value: BackendProdSettings,
        }
        SettingsClass = settings_classes.get(self.environment, BackendProdSettings)

        if config_data:
            config_data["CONFIG_SOURCE"] = "consul"
            return SettingsClass(**config_data)
        else:
            logger.info(f"Using fallback configuration from '.env-local' for {self.environment} environment.")
            settings = SettingsClass(_env_file=".env-local")
            settings.CONFIG_SOURCE = "fallback (.env-local)"
            return settings

@lru_cache()
def get_settings() -> BackendBaseSettings:
    """
    A factory function to create and cache the settings object.

    This is the main entry point for accessing configuration. It fetches config
    from Consul and then uses a factory to instantiate the correct settings
    class for the current environment (DEV, STG, PROD).
    """
    logger.info("CONFIGURING APP configuration | Fetching config from Consul...")
    consul_config = _fetch_config_from_consul()
    environment = os.getenv("ENVIRONMENT", "DEV")
    logger.info(f"ENVIRONMENT set to: '{environment}'.")

    factory = BackendSettingsFactory(environment=environment)
    return factory(config_data=consul_config)

settings: BackendBaseSettings = get_settings()