"""test_quiz_word_dao.py"""


from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.database.quiz_word_dao import QuizWordDAO


@pytest.fixture
def quiz_word_dao():
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        quiz_word_dao = QuizWordDAO(db_path)
        yield quiz_word_dao



# Need a fixture to read entries in the table of certain column
# ie the "read from column" in quiz_word


def test_added_num_correct_successfully():
    pass


def test_added_num_incorrect_successfully():
    pass


def test_increased_level_successfully():
    pass


def test_reset_level_successfully():
    pass


def test_set_word_as_known_successfully():
