from pydantic import (
    Field,
    PostgresDsn,
    RedisDsn,
    SecretStr
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_dsn: PostgresDsn | str = "sqlite+aiosqlite:///db.db" #  I use sqlite for development
    app_title: str = "FastAPI template"
    version: str = "0.1.0"
    
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    


settings = Settings()
