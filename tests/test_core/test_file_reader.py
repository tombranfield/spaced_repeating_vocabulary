"""
Testing file_reader.py in src/core
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.file_reader import FileReader
from src.database.exception import EmptyWordListException


THIS_DIR = Path(__file__).parent
VALID_FILE_PATH = THIS_DIR / "valid_input.dat"
INVALID_MISSING_COLUMN_PATH = THIS_DIR / "invalid_missing_column.dat"
INVALID_EXTRA_COLUMN_PATH = THIS_DIR / "invalid_extra_column.dat"
EMPTY_FILE_PATH = THIS_DIR / "empty_input.dat"


@pytest.fixture
def file_reader():
    with TemporaryDirectory() as tmp_dir:
        db_path = str(Path(tmp_dir)) + "temp_db.db"
        file_reader = FileReader("", db_path)
        yield file_reader


def test_file_data_successfully_added_to_database(file_reader):
    file_reader.file_path = VALID_FILE_PATH
    file_reader.insert_into_database("Harry Potter und der Stein der Weisen", "German")


def test_invalid_file_with_missing_value_raises_an_exception(file_reader):
    file_reader.file_path = INVALID_MISSING_COLUMN_PATH
    with pytest.raises(IndexError):
        file_reader.insert_into_database("My Word List", "German")


def test_invalid_file_with_third_column_raises_exception(file_reader):
    file_reader.file_path = INVALID_EXTRA_COLUMN_PATH
    with pytest.raises(ValueError):
        file_reader.insert_into_database("My Word List", "German")


def test_file_path_successfully_inserted(file_reader):
    file_reader.file_path = VALID_FILE_PATH


def test_raise_exception_for_missing_file(file_reader):
    input_file_path = "nonsense_non-existent_file.txt"
    file_reader.file_path = input_file_path
    with pytest.raises(FileNotFoundError):
        file_reader.insert_into_database("My Word List", "German")


def test_raise_exception_if_no_filepath_specified(file_reader):
    with pytest.raises(FileNotFoundError):
        file_reader.insert_into_database("My Word List", "German")


def test_check_empty_file_is_recognized_as_empty(file_reader):
    empty_file_path = EMPTY_FILE_PATH
    file_reader.file_path = empty_file_path
    with pytest.raises(EmptyWordListException):
        file_reader.insert_into_database("My Word List", "German")    

