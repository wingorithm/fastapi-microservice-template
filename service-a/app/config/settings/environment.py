import enum

class Environment(str, enum.Enum):
    PRODUCTION: str = "PROD"
    DEVELOPMENT: str = "DEV"
    STAGING: str = "STAGE"  