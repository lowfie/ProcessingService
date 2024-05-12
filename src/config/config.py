import os
from typing import Any, Type
from functools import partial

import yaml
from src.config.settings import BASE_DIR
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource


DEFAULT_PATH = str(BASE_DIR) + "/src/config/files/dev.yaml"


class JWTConfig(BaseSettings):
    secret_key: str
    algorithm: str


class AdminConfig(BaseSettings):
    name: str
    password: str


class Config(BaseSettings):
    admin: AdminConfig
    jwt: JWTConfig

    @staticmethod
    def _yaml_config_settings_resource_source(path: str | None) -> dict[str, Any]:
        if not path or not os.path.exists(path):
            return dict()
        with open(path) as file:
            config = yaml.safe_load(file)
        return config

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (
            env_settings,
            partial(cls._yaml_config_settings_resource_source, path=DEFAULT_PATH),
            init_settings,
            file_secret_settings
        )
