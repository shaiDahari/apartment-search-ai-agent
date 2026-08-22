"""Tests for SQLAlchemy database configuration."""

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from src.database.config import (
    DATABASE_DRIVER,
    REQUIRED_ENVIRONMENT_VARIABLES,
    DatabaseConfig,
    DatabaseConfigError,
    build_database_url,
    create_database_engine,
    create_session_factory,
)


def clear_database_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove database configuration variables for isolated tests."""

    for variable_name in REQUIRED_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable_name, raising=False)


def set_database_environment(
    monkeypatch: pytest.MonkeyPatch,
    *,
    host: str = "127.0.0.1",
    port: str = "3307",
    database: str = "apartment_search_ai_agent",
    user: str = "apartment_app",
    password: str = "test-password",
) -> None:
    """Set complete database configuration in the test environment."""

    monkeypatch.setenv("MYSQL_HOST", host)
    monkeypatch.setenv("MYSQL_PORT", port)
    monkeypatch.setenv("MYSQL_DATABASE", database)
    monkeypatch.setenv("MYSQL_USER", user)
    monkeypatch.setenv("MYSQL_PASSWORD", password)


def test_from_env_reads_complete_database_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that complete environment settings create a config object."""

    clear_database_environment(monkeypatch)
    set_database_environment(monkeypatch)

    config = DatabaseConfig.from_env(load_environment=False)

    assert config.host == "127.0.0.1"
    assert config.port == 3307
    assert config.database == "apartment_search_ai_agent"
    assert config.user == "apartment_app"
    assert config.password == "test-password"


def test_from_env_rejects_missing_required_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that missing settings fail with a clear error."""

    clear_database_environment(monkeypatch)
    set_database_environment(monkeypatch)
    monkeypatch.delenv("MYSQL_DATABASE")

    with pytest.raises(DatabaseConfigError, match="MYSQL_DATABASE"):
        DatabaseConfig.from_env(load_environment=False)


def test_from_env_rejects_empty_required_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that blank settings are treated as missing."""

    clear_database_environment(monkeypatch)
    set_database_environment(monkeypatch, user="   ")

    with pytest.raises(DatabaseConfigError, match="MYSQL_USER"):
        DatabaseConfig.from_env(load_environment=False)


def test_from_env_rejects_non_integer_port(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify that the MySQL port must be an integer."""

    clear_database_environment(monkeypatch)
    set_database_environment(monkeypatch, port="not-a-number")

    with pytest.raises(DatabaseConfigError, match="MYSQL_PORT must be an integer"):
        DatabaseConfig.from_env(load_environment=False)


def test_build_database_url_uses_mysql_pymysql_driver() -> None:
    """Verify that URL construction uses the approved MySQL driver."""

    config = DatabaseConfig(
        host="127.0.0.1",
        port=3307,
        database="apartment_search_ai_agent",
        user="apartment_app",
        password="test-password",
    )

    url = build_database_url(config)

    assert url.drivername == DATABASE_DRIVER
    assert url.username == "apartment_app"
    assert url.password == "test-password"
    assert url.host == "127.0.0.1"
    assert url.port == 3307
    assert url.database == "apartment_search_ai_agent"


def test_rendered_database_url_hides_password() -> None:
    """Verify that the default rendered URL does not expose the password."""

    config = DatabaseConfig(
        host="127.0.0.1",
        port=3307,
        database="apartment_search_ai_agent",
        user="apartment_app",
        password="test-password",
    )

    rendered_url = str(build_database_url(config))

    assert "test-password" not in rendered_url
    assert "***" in rendered_url


def test_create_database_engine_does_not_connect() -> None:
    """Verify that engine creation returns a lazy SQLAlchemy engine."""

    config = DatabaseConfig(
        host="127.0.0.1",
        port=3307,
        database="apartment_search_ai_agent",
        user="apartment_app",
        password="test-password",
    )

    engine = create_database_engine(config)

    assert isinstance(engine, Engine)
    assert engine.url.drivername == DATABASE_DRIVER


def test_create_session_factory_binds_to_engine() -> None:
    """Verify that session factory creation binds to the provided engine."""

    config = DatabaseConfig(
        host="127.0.0.1",
        port=3307,
        database="apartment_search_ai_agent",
        user="apartment_app",
        password="test-password",
    )
    engine = create_database_engine(config)

    session_factory = create_session_factory(engine=engine)

    assert isinstance(session_factory, sessionmaker)
    assert session_factory.kw["bind"] is engine
