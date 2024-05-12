from pathlib import Path

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core.core_schema import FieldValidationInfo

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_DSN: PostgresDsn | None = None

    UVICORN_USE_COLORS: bool
    UVICORN_RELOAD: bool
    UVICORN_ACCESS_LOG: bool
    UVICORN_WORKERS: int
    UVICORN_HOST: str
    UVICORN_PORT: int
    UVICORN_FORWARDED_ALLOW_IPS: str
    UVICORN_PROXY_HEADERS: bool

    DOCKER_EXPOSE_PORT: int

    @field_validator("POSTGRES_DSN")
    @classmethod
    def assemble_db_connection(
            cls, value: PostgresDsn | None,
            values: FieldValidationInfo
    ) -> PostgresDsn:
        if isinstance(value, str):
            return value

        postgres_url = "{schema}://{user}:{password}@{host}:{port}/{db}".format(
            schema="postgresql+asyncpg",
            user=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            port=values.data.get("POSTGRES_PORT"),
            db=values.data.get("POSTGRES_DB")
        )
        return postgres_url
