"""
Testing database.py
"""

import database
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory


@pytest.fixture
def empty_db():
    with TemporaryDirectory() as db_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(db_dir)) + db_name
        db = database.Database(db_path)
        yield db

def test_database_is_created(empty_db):
    num_words_in_db = empty_db.total_words()
    assert num_words_in_db == 0

def test_database_insert_word(empty_db):
    num_words_before = empty_db.total_words()
    empty_db.insert_word("bullig", "cheap", "german", 
                    "Harry Potter und der Stein der Weisen")
    num_words_after = empty_db.total_words()
    assert num_words_before == 0 and num_words_after == 1
