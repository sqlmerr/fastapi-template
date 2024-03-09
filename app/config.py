import os
import dotenv

from typing import Optional, Union, List
from dataclasses import dataclass, field


dotenv.load_dotenv()


@dataclass
class DbSettings:
    host: str
    port: int
    user: str
    name: str
    password: str
    _url: str = ""

    @property
    def url(self) -> str:
        if not self._url:
            self._url = f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        self._url = value


@dataclass
class Settings:
    db: DbSettings
    secret_key: str
    app_title: str = "FastAPI template"
    version: str = "0.1.0"
    backend_cors_origins: List[str] = field(
        default_factory=lambda: list("localhost:3000")
    )
    development: bool = True


def get_env_str(name: str, default: Optional[Union[str, int]] = None):
    value = os.getenv(name, default)
    if not value:
        raise ValueError(f"no value in .env named {name}")
    return value


def get_settings() -> Settings:
    db = DbSettings(
        get_env_str("POSTGRES_HOST", "localhost"),
        get_env_str("POSTGRES_PORT", 5432),
        get_env_str("POSTGRES_USER", "postgres"),
        get_env_str("POSTGRES_NAME", "postgres"),
        get_env_str("POSTGRES_PASSWORD", "postgres"),
    )
    settings = Settings(db, get_env_str("SECRET_KEY"))
    if settings.development is True:
        settings.db.url = "sqlite+aiosqlite:///db.db"
    return settings


settings = get_settings()
