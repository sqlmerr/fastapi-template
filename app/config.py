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

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class Settings:
    db: DbSettings
    app_title: str = "FastAPI template"
    version: str = "0.1.0"
    backend_cors_origins: List[str] = field(
        default_factory=lambda: list("localhost:3000")
    )


def get_env_str(name: str, default: Optional[Union[str, int]] = None):
    value = os.getenv(name, default)
    if not value:
        raise ValueError(f"no value in .env named {name}")
    return value


def get_settings() -> Settings:
    return Settings(
        DbSettings(
            get_env_str("POSTGRES_HOST", "localhost"),
            get_env_str("POSTGRES_PORT", 5432),
            get_env_str("POSTGRES_USER", "postgres"),
            get_env_str("POSTGRES_NAME", "postgres"),
            get_env_str("POSTGRES_PASSWORD", "postgres"),
        )
    )


settings = get_settings()
