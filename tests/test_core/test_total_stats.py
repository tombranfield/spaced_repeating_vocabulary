"""test_total_stats.py"""


from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.total_stats import TotalStats
from src.core.word_list import WordList
from src.database.database import Database


def test_can_initialize_total_stats_successfully(total_stats):



@pytest.fixture
def database():
    with TemporaryDirectory() as tmp_dir:
        db_path = str(Path(tmp_dir)) + "temp_db.db"
        database = Database(db_path)
        yield database


@pytest.fixture
def word_list_1():
    pair_1 = WordPair("hallo", "hello")
    pair_2 = WordPair("auf wiedersehen", "goodbye")
    pair_3 = WordPair("danke", "thank you")
    pair_4 = WordPair("das Brot, -", "bread")
    pair_5 = WordPair("der Wein, -", "wine")
    wordpairs = (pair_1, pair_2, pair_3)
    word_list = WordList("My List", "German", wordpairs)
    return word_list


@pytest.fixture
def word_list_2():
    pair_1 = WordPair("bonjour", "hello")
    pair_2 = WordPair("merci", "thank you")
    pair_3 = WordPair("au revoir", "goodbye")
    wordpairs = (pair_1, pair_2, pair_3)
    word_list = WordList("Starter French Words", "French", wordpairs)
    return word_list


@pytest.fixture
def db_with_new_words(database, word_list_1, word_list_2):
    word_list_dao = WordListDAO(database._db_path)
    word_list_dao.insert_word_list(word_list_1)    
    word_list_dao.insert_word_list(word_list_2)    
    yield database
