"""test_courses_dao.py"""


from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.database.courses_dao import CoursesDAO
from src.database.exception import DuplicateEntryException


@pytest.fixture
def courses_dao():
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        row_dao = RowDAO(db_path)
        yield row_dao


