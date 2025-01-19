import os
from pathlib import Path
from typing import Final, List, Optional, Union

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PathLike = Union[os.PathLike[str], str, Path]


LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
PROJECT_NAME = os.getenv("PROJECT_NAME", "app")
PROJECT_VERSION = os.getenv("PROJECT_VERSION", "0.0.1")

LOGGING_FORMAT: Final[str] = "%(asctime)s %(name)s %(levelname)s -> %(message)s"
DATETIME_FORMAT: Final[str] = "%Y.%m.%d %H:%M"


def root_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def path(*paths: _PathLike, base_path: Optional[_PathLike] = None) -> str:
    if base_path is None:
        base_path = root_dir()

    return os.path.join(base_path, *paths)


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="DB_",
        extra="ignore",
        env_file="./.env",
    )

    uri: str = Field(default="")
    name: str = Field(default="")
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    connection_pool_size: int = 10
    connection_max_overflow: int = 90
    connection_pool_pre_ping: bool = True

    @property
    def url(self) -> str:
        if "sqlite" in self.uri:
            return self.uri.format(self.name)
        return self.uri.format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.name,
        )


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="REDIS_",
        extra="ignore",
    )

    host: str = "127.0.0.1"
    port: int = 6379
    password: Optional[str] = None


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="SERVER_",
        extra="ignore",
    )
    methods: List[str] = ["*"]
    headers: List[str] = ["*"]
    origins: List[str] = ["*"]
    host: str = "127.0.0.1"
    port: int = 8080


class CipherSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        case_sensitive=False,
        env_prefix="CIPHER_",
        extra="ignore",
    )
    algorithm: str = ""
    secret_key: str = ""
    public_key: str = ""
    access_token_expire_seconds: int = 7200
    refresh_token_expire_seconds: int = 604800


class AesCipherSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        case_sensitive=False,
        env_prefix="AESCIPHER_",
        extra="ignore",
    )
    secret_key: str = ""


class FixedFloatSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        case_sensitive=False,
        env_prefix="HUOBI_",
        extra="ignore",
    )
    secret_token: str = ""
    access_token: str = ""
    base_url: str = ""


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        case_sensitive=False,
        env_prefix="BOT_",
        extra="ignore",
    )
    token: str = ""


class TronSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="TRON_",
        extra="ignore",
    )

    grid_api: str = ""


class Settings(BaseSettings):
    db: DatabaseSettings
    redis: RedisSettings
    server: ServerSettings
    ciphers: CipherSettings
    aescipher: AesCipherSettings
    ff: FixedFloatSettings
    bot: BotSettings
    tron: TronSettings


def load_settings(
    db: Optional[DatabaseSettings] = None,
    redis: Optional[RedisSettings] = None,
    server: Optional[ServerSettings] = None,
    ciphers: Optional[CipherSettings] = None,
    ff: Optional[FixedFloatSettings] = None,
    bot: Optional[BotSettings] = None,
    tron: Optional[TronSettings] = None,
    aescipher: Optional[AesCipherSettings] = None,
) -> Settings:
    return Settings(
        db=db or DatabaseSettings(),
        redis=redis or RedisSettings(),
        server=server or ServerSettings(),
        ciphers=ciphers or CipherSettings(),
        ff=ff or FixedFloatSettings(),
        bot=bot or BotSettings(),
        tron=tron or TronSettings(),
        aescipher=aescipher or AesCipherSettings(),
    )
