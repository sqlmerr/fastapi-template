from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: SecretStr
    secret_key: SecretStr
    app_title: str = "FastAPI template"
    version: str = "0.1.0"
    backend_cors_origins: List[str] = ["localhost:3000"]
    development: bool = True


settings = Settings()
