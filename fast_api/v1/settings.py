import os
from dataclasses import asdict, dataclass, field
from logging import getLogger
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

from fast_api.v1.exceptions import EnvironmentNotFoundException

logger = getLogger(__name__)


@dataclass
class PostgresConnection:
    drivername: str
    username: str
    password: str
    host: str
    port: str
    database: str


@dataclass
class Settings:
    env: str
    middlewares: Optional[list] = None
    connection: Optional[PostgresConnection] = None


def ProductionSettings() -> Settings:
    return Settings(
        env="prod",
        middlewares=[],
    )


def DevelopmentSettings() -> Settings:
    return Settings(
        env="dev",
        middlewares=[],
    )


def DockerSettings() -> Settings:
    return Settings(
        env="docker",
        middlewares=[],
        connection=PostgresConnection(
            drivername="postgresql+pg8000",
            username="postgres",
            password="postgres",
            host="postgres",
            port=5432,
            database="postgres",
        ),
    )


@dataclass
class Environments:
    prod: Settings = field(default_factory=ProductionSettings())
    dev: Settings = field(default_factory=DevelopmentSettings())
    docker: Settings = field(default_factory=DockerSettings())


def _get_environments() -> Environments:
    return Environments(
        prod=ProductionSettings(),
        dev=DevelopmentSettings(),
        docker=DockerSettings(),
    )


def get_settings(env: str = None) -> Settings:
    environments = _get_environments()
    if env:
        try:
            return getattr(environments, env)
        except AttributeError:
            raise EnvironmentNotFoundException("Requested environment does not exist.")
    try:
        e = os.environ["ENV"]
        return getattr(environments, e)
    except KeyError:
        logger.warning("[!] Environment is not defined, defaulting to docker")
        return DockerSettings()


SETTINGS = get_settings()
ENGINE = create_engine(URL.create(**asdict(SETTINGS.connection)))
SESSION = sessionmaker(ENGINE)