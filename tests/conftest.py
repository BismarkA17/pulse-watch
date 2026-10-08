import os

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://pulsewatch:pulsewatch@localhost:5432/pulsewatch_test",
)

from alembic import command
from alembic.config import Config

command.upgrade(Config("alembic.ini"), "head")

import pytest

from pulsewatch.api import conn


@pytest.fixture(autouse=True)
def clean_tables():
    conn.execute("TRUNCATE metrics, incidents RESTART IDENTITY")

