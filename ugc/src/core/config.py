from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Base dir of UGC service
BASE_DIR = Path(__file__).parent.parent.parent


class KafkaSettings(BaseSettings):
    producer: str = 'kafka-0:9092'
    topic: str = 'events'

    model_config = SettingsConfigDict(
        env_prefix='kafka_',
        env_file=BASE_DIR / '.env',
        extra='ignore',
    )


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str = 'WowSoSecret'
    AUTHAPI: str = 'http://authapi:8000/authapi/api/v1/users/profile'

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        extra='ignore',
    )


class MongoDBSettings(BaseSettings):
    INITDB_DATABASE: str = ...
    URI: str = ...

    model_config = SettingsConfigDict(
        env_prefix='mongo_',
        env_file=BASE_DIR / '.env',
        extra='ignore',
    )


class SentrySettings(BaseSettings):
    URL: str = ...

    model_config = SettingsConfigDict(
        env_prefix='sentry_',
        env_file=BASE_DIR / '.env',
        extra='ignore',
    )


class EventAPISettings(BaseSettings):
    FLASK_APP: str = ...
    FLASK_PORT: int = ...
    FLASK_DEBUG: bool = ...
    SECRET_KEY: str = ...

    kafka: KafkaSettings = KafkaSettings()
    auth: AuthSettings = AuthSettings()
    mongo: MongoDBSettings = MongoDBSettings()
    sentry: SentrySettings = SentrySettings()

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        extra='ignore',
    )


settings = EventAPISettings()
