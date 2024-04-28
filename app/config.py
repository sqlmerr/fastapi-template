from typing import List, Optional

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: SecretStr
    test_db_url: Optional[SecretStr] = None
    secret_key: SecretStr
    app_title: str = "FastAPI template"
    version: str = "0.1.0"
    backend_cors_origins: List[str] = ["localhost:3000"]
    development: bool = True

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()
