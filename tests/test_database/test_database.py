"""
Testing database.py
"""

# OK pytest.ini isn't working
import database
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory


# A fixture that creates an empty database
# in a temporary directory for testing purposes
# Read the cards source code for more
@pytest.fixture
def empty_db():
    with TemporaryDirectory() as db_dir:
        db_path = str(Path(db_dir))
        temp_db = database.Database(db_path)


# Test that the database is created
def test_database_is_created(empty_db):
    print("yo")



def test_one_equals_one():
    a = 1
    assert a == 1
