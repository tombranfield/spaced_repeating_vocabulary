"""test_quiz_word_dao.py"""


from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.word_pair import WordPair
from src.core.quiz_word import QuizWord
from src.database.quiz_word_dao import QuizWordDAO



@pytest.fixture
def quiz_word():
    id = 101
    word_pair = WordPair("hallo", "hello")
    quiz_word = QuizWord(id, word_pair)
    return quiz_word


@pytest.fixture
def quiz_word_dao(quiz_word):
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        quiz_word_dao = QuizWordDAO(quiz_word, db_path)
        yield quiz_word_dao


# TODO need to add quiz_word to the database!
# Otherwise there is no record to read or update of it


def test_instantiated_quiz_word_dao_successfully(quiz_word_dao):
    pass


def test_added_num_correct_successfully():
    print("current word:", quiz_word_dao.quiz_word.foreign_word)
    num_correct_before = quiz_word_dao._get_column_value("num_correct")
    print("num_correct_before:", num_correct_before)
    pass


def test_added_num_incorrect_successfully():
    pass


def test_increased_level_successfully():
    pass


def test_reset_level_successfully():
    pass


def test_set_word_as_known_successfully():
    pass
