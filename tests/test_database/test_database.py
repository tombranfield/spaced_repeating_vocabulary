"""
Testing database.py
"""

# OK pytest.ini isn't working
import database
import pytest


# A fixture that creates an empty database
# in a temporary directory for testing purposes
@pytest.fixture
def empty_db():
    temp_db_filename = "/tempdir/"
    temp_db = Database(temp_db_path)


# Test that the database is created
def test_database_is_created():
    print("yo")



def test_one_equals_one():
    a = 1
    assert a == 1
