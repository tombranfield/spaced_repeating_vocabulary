"""
Testing file_reader.py in src/core
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.file_reader import FileReader


# Need a valid file
# Need an invalid file
# Need a temporary db_location (add db location to FileReader!)
# Need a FileReader fixture

@pytest.fixture
def file_reader():
    with TemporaryDirectory() as tmp_dir:
        db_path = str(Path(tmp_dir)) + "temp_db.db"
        file_reader = FileReader("input_file.txt", db_path)
        yield file_reader


def test_valid_file_classified_as_valid():
    # return True
    pass


def test_invalid_file_classified_as_invalid():
    # return True
    pass


def test_file_path_successfully_read(file_reader):
    assert file_reader.file_path == "input_file.txt"


def test_file_path_successfully_changed():
    pass


def test_file_data_added_to_database():
    pass


