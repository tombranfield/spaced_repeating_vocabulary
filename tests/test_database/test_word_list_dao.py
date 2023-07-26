"""
Testing word_list_dao.py
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.database.word_list_dao import WordListDAO


@pytest.fixture
def word_list_dao():
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        word_list_dao = WordListDAO(db_path)
        yield word_list_dao


@pytest.fixture
def word_list():
    words = (WordPair("bullig", "cheap"), WordPair("danke", "thank you"))
    word_list = WordList("My Word List", "German", words)
    return word_list


def test_word_list_dao_creates_db(word_list_dao):
    num_rows = word_list_dao.db.total_rows()
    assert num_rows == 0


"""
def test_row_dao_inserts_rows_successfully(row_dao, row_of_data):
    pass

def test_row_insert_row_inserts_correct_data(row_dao, row_of_data):
    pass

def test_row_dao_correct_default_values_on_insertion(row_dao, row_of_data):
    pass


def test_inserts_multiple_row_in_succession(row_dao, rows_of_data):
    pass

def test_row_dao_one_row_db(row_dao_one_row_db):
    pass

def test_is_word_already_there(row_dao_one_row_db, row_of_data):
    pass

def test_is_word_not_there(row_dao_one_row_db, row_of_data):
    pass

def test_delete_word_list(row_dao_one_row_db, row_of_data):
    pass
"""
