from typing import Literal

from common.cache.settings import CacheSettings
from common.database.settings import DatabaseSettings
from common.settings import CONFIG_PATH, YamlSettings
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class AppSettings(YamlSettings):
    name: str
    host: str
    port: int
    env: Literal["prod", "dev"]

    model_config = SettingsConfigDict(yaml_file=CONFIG_PATH, yaml_config_section="app")


class AuthDatabaseSettings(YamlSettings, DatabaseSettings):
    model_config = SettingsConfigDict(yaml_file=CONFIG_PATH, yaml_config_section="database")


class AuthCacheSettings(YamlSettings, CacheSettings):
    model_config = SettingsConfigDict(yaml_file=CONFIG_PATH, yaml_config_section="cache")



class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    database: AuthDatabaseSettings = AuthDatabaseSettings()
    cache: AuthCacheSettings = AuthCacheSettings()
