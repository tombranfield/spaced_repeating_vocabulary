"""
Testing word_list_dao.py
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.database.exception import EmptyWordListException
from src.database.word_list_dao import WordListDAO


@pytest.fixture
def word_list_dao():
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        word_list_dao = WordListDAO(db_path)
        yield word_list_dao


@pytest.fixture
def word_pairs():
    word_pairs = (
        WordPair("hallo", "hello"),
        WordPair("auf wiedersehen", "goodbye"),
        WordPair("danke", "thank you"),
    )
    return word_pairs


@pytest.fixture
def word_list(word_pairs):
    word_list = WordList("My Word List", "German", word_pairs)
    return word_list


@pytest.fixture
def empty_word_list():
    word_list = WordList("My Empty Word List", "German")
    return word_list


def test_word_list_dao_creates_db(word_list_dao):
    num_rows = word_list_dao.db.total_rows()
    assert num_rows == 0


def test_insert_word_list_successfully(word_list_dao, word_list):
    word_list_dao.insert_word_list(word_list)
    num_rows = word_list_dao.db.total_rows()
    assert num_rows == word_list.num_words()


def test_delete_word_list_successfully(word_list_dao, word_list):
    word_list_dao.insert_word_list(word_list)
    word_list_dao.delete_word_list(word_list.name)
    num_rows = word_list_dao.db.total_rows()
    assert num_rows == 0


def test_insert_word_list_inserts_correct_data(word_list_dao, word_list, word_pairs):
    word_list_dao.insert_word_list(word_list)

    list_name = word_list.name
    lang = word_list.language

    for word_pair in word_pairs:
        f_word = word_pair.foreign_word
        t_word = word_pair.translated_word        

        out_foreign_word = word_list_dao._column_value("foreign_word", f_word, list_name)
        out_trans_word = word_list_dao._column_value("translated_word", f_word, list_name)
        out_language = word_list_dao._column_value("language", f_word, list_name)
        out_list_name = word_list_dao._column_value("word_list_name", f_word, list_name)

        assert out_foreign_word == f_word
        assert out_trans_word == t_word
        assert out_language == lang
        assert out_list_name == list_name


def test_inserting_word_list_has_correct_default_values(word_list_dao, word_list):
    pass


def test_inserts_multiple_word_lists_in_succession(word_list_dao, word_list):
    pass


def test_know_that_word_already_in_db(word_list_dao, word_list):
    pass


def test_word_correctly_identified_as_not_in_db(word_list_dao, row_of_data):
    pass


def test_inserting_an_empty_word_list_fails(word_list_dao, empty_word_list):
    with pytest.raises(EmptyWordListException):
        word_list_dao.insert_word_list(empty_word_list)        


def test_making_and_inserting_an_invalid_list_fails(word_list_dao):
    with pytest.raises(Exception):
        broken_word_list = WordList("", '')
        world_list_dao.insert_word_list(broken_word_list)
