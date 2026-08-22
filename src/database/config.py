"""SQLAlchemy database configuration for the application.

This module builds reusable SQLAlchemy connection objects from environment
variables. It does not connect eagerly, create tables, define ORM models, or
run database schema changes.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

REQUIRED_ENVIRONMENT_VARIABLES = (
    "MYSQL_HOST",
    "MYSQL_PORT",
    "MYSQL_DATABASE",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
)

DATABASE_DRIVER = "mysql+pymysql"


class DatabaseConfigError(RuntimeError):
    """Raised when required database configuration is missing or invalid."""


@dataclass(frozen=True)
class DatabaseConfig:
    """Database connection settings loaded from environment variables."""

    host: str
    port: int
    database: str
    user: str
    password: str

    @classmethod
    def from_env(cls, *, load_environment: bool = True) -> "DatabaseConfig":
        """Build database configuration from environment variables.

        A local ``.env`` file is loaded for development convenience. Tests can
        still isolate configuration by patching environment variables.
        """

        if load_environment:
            load_dotenv()

        values = {
            variable_name: os.environ.get(variable_name)
            for variable_name in REQUIRED_ENVIRONMENT_VARIABLES
        }
        missing_variables = [
            variable_name
            for variable_name, value in values.items()
            if value is None or value.strip() == ""
        ]

        if missing_variables:
            joined_variables = ", ".join(missing_variables)
            raise DatabaseConfigError(
                f"Missing required database configuration: {joined_variables}"
            )

        raw_port = values["MYSQL_PORT"]
        assert raw_port is not None

        try:
            port = int(raw_port)
        except ValueError as error:
            raise DatabaseConfigError(
                "MYSQL_PORT must be an integer"
            ) from error

        return cls(
            host=values["MYSQL_HOST"] or "",
            port=port,
            database=values["MYSQL_DATABASE"] or "",
            user=values["MYSQL_USER"] or "",
            password=values["MYSQL_PASSWORD"] or "",
        )


def build_database_url(config: DatabaseConfig) -> URL:
    """Build the SQLAlchemy URL for the configured MySQL database."""

    return URL.create(
        drivername=DATABASE_DRIVER,
        username=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database,
    )


def create_database_engine(config: DatabaseConfig | None = None) -> Engine:
    """Create a reusable SQLAlchemy engine.

    SQLAlchemy engines are lazy; this function creates the engine object but
    does not open a database connection by itself.
    """

    database_config = config or DatabaseConfig.from_env()
    return create_engine(build_database_url(database_config))


def create_session_factory(
    engine: Engine | None = None,
    config: DatabaseConfig | None = None,
) -> sessionmaker[Session]:
    """Create a reusable SQLAlchemy session factory."""

    database_engine = engine or create_database_engine(config)
    return sessionmaker(bind=database_engine)
