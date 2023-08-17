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
    wordpairs = (pair_1, pair_2, pair_3, pair_4, pair_5)
    word_list = WordList("My List", "German", wordpairs)
    return word_list


@pytest.fixture
def db_with_new_words(database, new_word_list):
    word_list_dao = WordListDAO(database._db_path)
    word_list_dao.insert_word_list(new_word_list)
    yield database


@pytest.fixture
def quiz_word_selector_new_words(db_with_new_words):
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
def quiz_word_selector_new_and_review_words(db_some_new_some_review):
    quiz_word_selector = QuizWordSelector("My List", db_some_new_some_review._db_path)
    return quiz_word_selector


def test_can_initialize_word_selector_successfully(quiz_word_selector_new_words):
    pass


def test_get_correct_words_to_learn_with_new_words(quiz_word_selector_new_words, new_word_list):
    out_quiz_words = quiz_word_selector_new_words.words_to_learn()
    new_word_pairs = new_word_list.word_pairs
    for index, quiz_word in enumerate(out_quiz_words, 1):
        assert quiz_word.id == index
        assert quiz_word.foreign_word == new_word_pairs[index-1].foreign_word
        assert quiz_word.translated_word == new_word_pairs[index-1].translated_word


def test_get_correct_words_to_review(quiz_word_selector_new_and_review_words):
    out_quiz_words = quiz_word_selector_new_and_review_words.words_to_review()    
    assert out_quiz_words[0].foreign_word == "hallo"
    assert out_quiz_words[1].foreign_word == "danke"
    assert len(out_quiz_words) == 2


def test_get_empty_list_of_words_to_review(quiz_word_selector_new_words):
    out_review_list = quiz_word_selector_new_words.words_to_review()
    assert len(out_review_list) == 0


def test_use_a_word_list_that_does_not_exist_in_database(database):
    quiz_word_selector = QuizWordSelector("Non-existant list", database._db_path)
    words_to_learn = quiz_word_selector.words_to_learn()
    words_to_review = quiz_word_selector.words_to_review()
    assert len(words_to_learn) == 0
    assert len(words_to_review) == 0


@pytest.mark.parametrize("i,expected", [(0,"hallo"), (1,"auf wiedersehen"), (2,"danke"), (3,"das Brot, -"), (4,"der Wein, -")]) 
def test_all_course_words_are_returned_successfully(quiz_word_selector_new_words, i, expected):
    all_course_words = quiz_word_selector_new_words.all_course_words()
    assert len(all_course_words) == 5
    assert all_course_words[i].foreign_word == expected
