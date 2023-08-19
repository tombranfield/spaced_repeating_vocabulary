"""test_quiz_word_dao.py"""


import datetime
from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.review_time_setter import ReviewTimeSetter
from src.core.row import Row
from src.core.word_pair import WordPair
from src.core.quiz_word import QuizWord
from src.database.row_dao import RowDAO
from src.database.quiz_word_dao import QuizWordDAO


@pytest.fixture
def quiz_word():
    id = 1
    word_pair = WordPair("hallo", "hello")
    quiz_word = QuizWord(id, word_pair)
    return quiz_word


@pytest.fixture
def quiz_word_dao(quiz_word):
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        
        row = Row(
            quiz_word.foreign_word, 
            quiz_word.translated_word,
            "German",
            "My Testing List"
        )
        row_dao = RowDAO(db_path)
        row_dao.insert_row(row)

        quiz_word_dao = QuizWordDAO(quiz_word, db_path)
        yield quiz_word_dao


@pytest.fixture
def datetime_mock(monkeypatch):
    
    MOCK_DATETIME = datetime.datetime(2012, 12, 25, 9, 0, 30)

    class mydatetime:
        @classmethod
        def now(cls):
            return MOCK_DATETIME

    monkeypatch.setattr(datetime, "datetime", mydatetime)


def test_instantiated_quiz_word_dao_successfully(quiz_word_dao):
    pass


def test_added_num_correct_successfully(quiz_word_dao):
    num_correct_before = quiz_word_dao._get_column_value("num_correct")
    quiz_word_dao.add_num_correct(2)
    num_correct_after = quiz_word_dao._get_column_value("num_correct")
    assert num_correct_before == 0
    assert num_correct_after == 2


def test_added_num_incorrect_successfully(quiz_word_dao):
    num_incorrect_before = quiz_word_dao._get_column_value("num_incorrect")
    quiz_word_dao.add_num_incorrect(2)
    num_incorrect_after = quiz_word_dao._get_column_value("num_incorrect")
    assert num_incorrect_before == 0
    assert num_incorrect_after == 2


def test_increased_level_successfully(quiz_word_dao):
    level_before = quiz_word_dao._get_column_value("level")
    quiz_word_dao.increase_level()
    level_after = quiz_word_dao._get_column_value("level")
    assert level_before == 1
    assert level_after == 2

def test_reset_level_successfully(quiz_word_dao):
    quiz_word_dao.increase_level()
    level_before = quiz_word_dao._get_column_value("level")
    quiz_word_dao.reset_level()
    level_after = quiz_word_dao._get_column_value("level")
    assert level_before == 2
    assert level_after == 1

def test_set_word_as_known_successfully(quiz_word_dao):
    is_known_before = quiz_word_dao._get_column_value("is_known")
    quiz_word_dao.set_word_as_known()
    is_known_after = quiz_word_dao._get_column_value("is_known")
    assert is_known_before == 0
    assert is_known_after == 1

def test_set_when_to_review_correctly(quiz_word_dao, datetime_mock):
    quiz_word_dao.set_when_to_review()
    current_level = quiz_word_dao._get_column_value("level")
    review_time_setter = ReviewTimeSetter(current_level)
    calc_next_review_time = review_time_setter.next_review_time()
    read_next_review_time = quiz_word_dao._get_column_value("when_review")
    assert calc_next_review_time == read_next_review_time

def test_set_when_to_review_correctly_after_increasing_level(quiz_word_dao, datetime_mock):
    for i in range(10):
        quiz_word_dao.increase_level()
    quiz_word_dao.set_when_to_review()
    current_level = quiz_word_dao._get_column_value("level")
    review_time_setter = ReviewTimeSetter(current_level)
    
    calc_next_review_time = review_time_setter.next_review_time()
    read_next_review_time = quiz_word_dao._get_column_value("when_review")

    assert calc_next_review_time == read_next_review_time


