from base64 import b64decode
from typing import Any

from peewee import SqliteDatabase, PostgresqlDatabase
import pytest

from database.config import (
    DATABASE_TYPE,
    DB_NAME,
    DB_HOST,
    DB_USER,
)
from database.database import TABLES, database_setup, database_teardown
from database.models.user import User
from database.models.app import App
from database.models.file_snapshot import FileSnapshot
from database.models.files import File
from database.models.development_steps import DevelopmentSteps

EMPTY_PNG = b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


@pytest.fixture
def db() -> SqliteDatabase | PostgresqlDatabase:
    """
    Set up a new empty initialized test database.

    In case of SQlite, the database is created in-memory. In case of PostgreSQL,
    the database should already exist and be empty.

    This fixture will create all the tables and run the test in an isolated transaction.
    which gets rolled back after the test. The fixture also drops all the tables at the
    end.
    """
    db = database_setup()
    yield db
    database_teardown(db)


@pytest.fixture
def user_app_step(db) -> tuple[User, App, DevelopmentSteps]:
    user = User.create(email="", password="")
    app = App.create(user=user)
    step = DevelopmentSteps.create(app=app, llm_response={})
    return user, app, step


def test_create_tables(db: SqliteDatabase | PostgresqlDatabase) -> None:
    """
    Test that database tables are created for all the models.
    """
    tables = db.get_tables()
    expected_tables = [table._meta.table_name for table in TABLES]
    assert set(tables) == set(expected_tables)


def test_create_user(db: SqliteDatabase | PostgresqlDatabase) -> None:
    """
    Test that a user can be created.
    """
    user = User.create(email="test@example.com", password="password")
    from_db = User.get(id=user.id)
    assert from_db.email == "test@example.com"


def test_create_app(db: SqliteDatabase | PostgresqlDatabase, user: User) -> None:
    """
    Test that an app can be created for a user.
    """
    app = App.create(user=user)
    from_db = App.get(id=app.id)
    assert from_db.user == user


def test_create_development_step(
    db: SqliteDatabase | PostgresqlDatabase, app: App
) -> None:
    """
    Test that a development step can be created for an app.
    """
    step = DevelopmentSteps.create(app=app, llm_response={})
    from_db = DevelopmentSteps.get(id=step.id)
    assert from_db.app == app


def test_create_file(
    db: SqliteDatabase | PostgresqlDatabase, app: App
) -> None:
    """
    Test that a file can be created for an app.
    """
    file = File.create(app=app, name="test", path="test", full_path="test")
    from_db = File.get(id=file.id)
    assert from_db.app == app


@pytest.mark.parametrize(
    ("content", "expected_content"),
    [
        ("ascii text", "ascii text"),
        ("non-ascii text: ščćž", "non-ascii text: ščćž"),
        ("with null byte \0", "with null byte \0"),
    ],
)
def test_file_snapshot_text(
    db: SqliteDatabase | PostgresqlDatabase,
    user_app_step: tuple[User, App, DevelopmentSteps],
    content: str,
    expected_content: str,
) -> None:
    user, app, step = user_app_step
    file = File.create(app=app, name="test", path="test", full_path="test")

    fs = FileSnapshot.create(
        app=app,
        development_step=step,
        file=file,
        content=content,
    )
    from_db = FileSnapshot.get(id=fs.id)
    assert from_db.content == expected_content


def test_file_snapshot_binary(
    db
