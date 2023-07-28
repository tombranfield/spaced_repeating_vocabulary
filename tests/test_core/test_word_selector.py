"""test_word_selector.py"""


from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.core.word_selector import WordSelector
from src.database.database import Database
from src.database.word_list_dao import WordListDAO


@pytest.fixture
def database():
    with TemporaryDirectory() as tmp_dir:
        db_path = str(Path(tmp_dir)) + "temp_db.db"
        database = Database(db_path)
        yield database

@pytest.fixture
def new_word_list():
    pair_1 = WordPair("hallo", "hello")
    pair_2 = WordPair("auf wiedersehen", "goodbye")
    pair_3 = WordPair("danke", "thank you")
    wordpairs = (pair_1, pair_2, pair_3)
    word_list = WordList("My List", "German", wordpairs)
    return word_list

@pytest.fixture
def db_with_words(database, new_word_list):
    word_list_dao = WordListDAO(database._db_path)
    word_list_dao.insert_word_list(new_word_list)
    yield database

@pytest.fixture
def word_selector(db_with_words):
    word_selector = WordSelector(db_with_words._db_path)
    return word_selector


def test_can_initialize_word_selector_successfully(word_selector):
    pass


@pytest.mark.curtest
def test_get_correct_words_to_learn(word_selector):
    out_word_list = word_selector.words_to_learn()
    words_to_learn = out_word_list.foreign_words()
    print("START")
    print(words_to_learn)
    print("END")


def test_get_correct_words_to_review():
    pass



def test_get_empty_list_of_words_to_learn():
    pass



def test_get_empty_list_of_words_to_review():
    pass



def test_use_a_word_list_that_does_not_exist_in_database():
    pass
