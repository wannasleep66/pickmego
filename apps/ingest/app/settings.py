from typing import Literal

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pydantic_settings.sources import YamlConfigSettingsSource

CONFIG_PATH = "/config/config.yml"


class YamlSettings(BaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


class AppSettings(YamlSettings):
    name: str
    host: str
    port: int
    env: Literal["prod", "dev"]

    model_config = SettingsConfigDict(yaml_file=CONFIG_PATH, yaml_config_section="app")


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
