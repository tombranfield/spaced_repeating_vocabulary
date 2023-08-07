"""test_quiz_word_selector.py"""


from pathlib import Path
import pytest
from tempfile import TemporaryDirectory


from src.core.quiz_word import QuizWord
from src.core.quiz_word_selector import QuizWordSelector
from src.core.word_list import WordList
from src.core.word_pair import WordPair
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
    pair_4 = WordPair("das Brot, -", "bread")
    pair_5 = WordPair("der Wein, -", "wine")
    wordpairs = (pair_1, pair_2, pair_3)
    word_list = WordList("My List", "German", wordpairs)
    return word_list

@pytest.fixture
def db_with_new_words(database, new_word_list):
    word_list_dao = WordListDAO(database._db_path)
    word_list_dao.insert_word_list(new_word_list)
    yield database

@pytest.fixture
def word_selector_new_words(db_with_new_words):
    quiz_word_selector = QuizWordSelector("My List", db_with_new_words._db_path)
    return quiz_word_selector


@pytest.fixture
def db_some_new_some_review(db_with_new_words):
    query = ("UPDATE " + db_with_new_words.table_name + " "
             + "SET is_known = 1, when_review = '26/12/2022 09:30:00'"
             + "WHERE foreign_word = 'hallo' or foreign_word = 'danke'")
    db_with_new_words.connect_and_execute(query)
    return db_with_new_words


@pytest.fixture
def word_selector_new_and_review_words(db_some_new_some_review):
    word_selector = WordSelector("My List", db_some_new_some_review._db_path)
    return word_selector


def test_can_initialize_word_selector_successfully(word_selector_new_words):
    pass

@pytest.mark.curtest
def test_get_correct_words_to_learn_with_new_words(word_selector_new_words, new_word_list):
    out_learn_list = word_selector_new_words.words_to_learn()
    words_to_learn = out_learn_list.foreign_words()
    assert words_to_learn == new_word_list.foreign_words()

"""
def test_get_correct_words_to_review(word_selector_new_and_review_words):
    out_review_list = word_selector_new_and_review_words.words_to_review()
    words_to_review = out_review_list.foreign_words()
    assert words_to_review == ("hallo", "danke")


def test_get_empty_list_of_words_to_review(word_selector_new_words):
    out_review_list = word_selector_new_words.words_to_review()
    words_to_review = out_review_list.foreign_words()
    assert words_to_review == ()


def test_use_a_word_list_that_does_not_exist_in_database(database):
    word_selector = WordSelector("Non-existant list", database._db_path)
    words_to_learn = word_selector.words_to_learn()
    words_to_review = word_selector.words_to_review()
    assert words_to_learn.foreign_words() == ()
    assert words_to_review.foreign_words() == ()
"""
