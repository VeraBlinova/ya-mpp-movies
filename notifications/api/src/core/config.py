from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class DataBaseSettings(BaseSettings):
    user: str = ...
    password: str = ...
    db: str = ...
    host: str = ...
    port: int = ...

    model_config = SettingsConfigDict(
        env_prefix="postgres_",
        env_file=BASE_DIR / ".env",
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
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

    @property
    def url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}//"


class NotifAPISettings(BaseSettings):
    project_name: str = "NotificationsAPI"  # Used in Swagger docs
    project_description: str = "Notifications API service"

    app_port: int = 8000
    debug: bool = False

    db: DataBaseSettings = DataBaseSettings()

    mq: MQSettings = MQSettings()

    model_config = SettingsConfigDict(
        env_prefix="api_",
        env_file=BASE_DIR / "api.env",
        extra="ignore",
    )


settings = NotifAPISettings()
