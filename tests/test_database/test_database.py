"""
Testing database.py
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

import src.database.database as database
import src.core.row as row


@pytest.fixture
def empty_db():
    with TemporaryDirectory() as db_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(db_dir)) + db_name
        db = database.Database(db_path)
        yield db

@pytest.fixture
def row_of_data():
    new_row = row.Row("bullig", "cheap", "german", 
              "Harry Potter und der Stein der Weisen")
    return new_row


def test_database_is_created(empty_db):
    num_rows_in_db = empty_db.total_rows()
    assert num_rows_in_db == 0

def test_database_insert_row(empty_db, row_of_data):
    num_rows_before = empty_db.total_rows()
    empty_db.insert_row(row_of_data)
    num_rows_after = empty_db.total_rows()
    assert num_rows_before == 0 and num_rows_after == 1
