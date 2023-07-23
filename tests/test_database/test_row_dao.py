"""
Testing row_dao.py
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.row import Row
from src.database.row_dao import RowDAO


@pytest.fixture
def row_dao_empty_db():
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        row_dao = RowDAO(db_path)
        yield row_dao


@pytest.fixture
def row_dao_one_row_db(row_dao_empty_db, row_of_data):
    row_dao_empty_db.insert_row(row_of_data)
    yield row_dao_empty_db



def test_row_dao_creates_db(row_dao_empty_db):
    num_rows = row_dao_empty_db.total_rows()
    assert num_rows == 0


def test_row_dao_insert_row(row_dao_empty_db, row_of_data):
    num_rows_before = row_dao_empty_db.total_rows()
    row_dao_empty_db.insert_row(row_of_data)
    num_rows_after = row_dao_empty_db.total_rows()
    assert num_rows_before == 0 and num_rows_after == 1


def test_row_dao_one_row_db(row_dao_one_row_db):
    num_rows = row_dao_one_row_db.total_rows()
    assert num_rows == 1


def test_is_word_already_there(row_dao_one_row_db, row_of_data):
    foreign_word = row_of_data.foreign_word
    assert row_dao_one_row_db.is_word_already_there(foreign_word) == True
