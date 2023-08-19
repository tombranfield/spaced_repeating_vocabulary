"""test_quiz_word_dao.py"""


from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

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


def test_instantiated_quiz_word_dao_successfully(quiz_word_dao):
    pass


def test_added_num_correct_successfully(quiz_word_dao):
    num_correct_before = quiz_word_dao._get_column_value("num_correct")
    quiz_word_dao.add_num_correct(2)
    num_correct_after = quiz_word_dao._get_column_value("num_correct")
    assert num_correct_before == 0
    assert num_correct_after == 2


def test_added_num_incorrect_successfully():
    pass


def test_increased_level_successfully():
    pass


def test_reset_level_successfully():
    pass


def test_set_word_as_known_successfully():
    pass
