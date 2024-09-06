from datetime import timedelta
from logging import config as logging_config
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

# Logger config
logging_config.dictConfig(LOGGING)

# Base dir of authapi service
BASE_DIR = Path(__file__).parent.parent.parent


class DataBaseSettings(BaseSettings):
    user: str = ...
    password: str = ...
    db: str = ...
    host: str = ...
    port: int = ...

    content_prefix: str = 'films/'

    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )

    @property
    def url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}'


class RedisSettings(BaseSettings):
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...
    db_number: int = 0

    model_config = SettingsConfigDict(
        env_prefix='redis_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )

    @property
    def url(self):
        return f'redis://{self.host}:{self.port}/{self.db_number}'
        # return f'redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_number}'


class JWTSettings(BaseSettings):
    # Using name with authjwt_ prefix here, otherwise
    # async-fastapi-jwt-auth doesn't find parameters by names
    authjwt_secret_key: str = 'WowSoSecret'
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {'access', 'refresh'}
    authjwt_access_expires: int = timedelta(minutes=15)
    authjwt_refresh_expires: int = timedelta(days=30)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )

class OTELSettings(BaseSettings):
    enable: bool = True
    host: str = 'jaeger-service'
    port: int = 6831

    model_config = SettingsConfigDict(
        env_prefix='otel_exporter_jeager_agent_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )


class AuthAPISettings(BaseSettings):
    project_name: str = 'AuthAPI'   # Used in Swagger docs
    project_description: str = 'Authorization API service'

    app_port: int = 8000
    debug: bool = False

    db: DataBaseSettings = DataBaseSettings()
    redis: RedisSettings = RedisSettings()
    jwt: JWTSettings = JWTSettings()

    request_id_needed: bool = True
    request_limit_per_minute: int = 20

    tracer: OTELSettings = OTELSettings()

    model_config = SettingsConfigDict(
        env_prefix='authapi_',
        env_file=BASE_DIR / 'api.env',
        extra='ignore',
    )


settings = AuthAPISettings()
