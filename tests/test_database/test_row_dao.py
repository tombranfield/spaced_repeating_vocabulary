"""
Testing row_dao.py
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.row import Row
from src.database.row_dao import RowDAO


@pytest.fixture
def row_of_data():
    row = Row("bullig", "cheap", "german",
              "Harry Potter und der Stein der Weisen")

@pytest.fixture
def row_dao_empty_db():
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        row_dao = RowDao(db_path)
        yield row_dao

def test_row_dao_creates_db(row_dao_empty_db):
    num_rows_in_db



def test_simple():
    a = 1
    assert a == 1
