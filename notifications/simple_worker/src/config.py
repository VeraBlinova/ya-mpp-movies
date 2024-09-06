from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseSettings):
    user: str = ...
    password: str = ...
    db: str = ...
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(
        env_prefix="postgres_",
        env_file="../.env",
        extra="ignore",
    )

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class MQSettings(BaseSettings):
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...
    exchange: str = "api"

    model_config = SettingsConfigDict(
        env_prefix="mq_",
        env_file="../.env",
        extra="ignore",
    )

    @property
    def url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}//"


class SMTPSettings(BaseSettings):
    user: str = ...
    password: str = ...
    server: str = ...
    port: int = ...

    model_config = SettingsConfigDict(
        env_prefix="smtp_",
        env_file="../.env",
        extra="ignore",
    )

    @property
    def url(self):
        return f"smtp://{self.user}:{self.password}@{self.host}:{self.port}"


class SimpleWorkerSettings(BaseSettings):

    db: DataBaseSettings = DataBaseSettings()
    mq: MQSettings = MQSettings()
    smtp: SMTPSettings = SMTPSettings()


settings = SimpleWorkerSettings()
