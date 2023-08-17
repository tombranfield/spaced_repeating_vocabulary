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
        courses_dao = CoursesDAO(db_path)
        yield courses_dao


def test_courses_dao_created_successfully(courses_dao):
    pass


def test_courses_list_with_no_list_returns_empty_list(courses_dao):
    courses_list = courses_dao.courses_list()
    assert courses_list == []


def test_deleting_a_course_when_it_doesnt_exit_does_nothing(courses_dao):
    courses_dao.delete_course("non-existent course")
    

def test_add_new_course_successfully(courses_dao):
    courses_dao.add_new_course("My Testing List", "German")


def test_add_new_course_appears_in_courses_list(courses_dao):
    courses_dao.add_new_course("My Testing List", "German")
    courses_list = courses_dao.courses_list()
    assert courses_list == ["My Testing List"]


def test_add_several_courses_appear_in_courses_list(courses_dao):
    courses_dao.add_new_course("List_1", "French")
    courses_dao.add_new_course("List_2", "French")
    courses_dao.add_new_course("List_3", "French")
    courses_list = courses_dao.courses_list()
    assert courses_list == ["List_1", "List_2", "List_3"]


def test_delete_course_successfully(courses_dao):
    courses_dao.add_new_course("My Testing Course", "German")
    before_courses_list = courses_dao.courses_list()
    courses_dao.delete_course("My Testing Course")
    after_courses_list = courses_dao.courses_list()
    assert before_courses_list == ["My Testing Course"]
    assert after_courses_list == []


def test_check_returns_false_when_checking_if_non_existent_course_exists(courses_dao):
    b = courses_dao._does_course_already_exist("non-existent course")
    assert b == False


def test_adding_test_that_already_exists_yields_exception(courses_dao):
    courses_dao.add_new_course("My Course", "German")
    with pytest.raises(DuplicateEntryException):
        courses_dao.add_new_course("My Course", "German")


def test_retrieves_correct_language_from_course(courses_dao):
    courses_dao.add_new_course("My Course", "German")
    assert courses_dao.language("My Course") == "German"


def test_calling_for_language_of_non_existent_list_yields_nothing(courses_dao):
    b = courses_dao.language("non-existent list")
    assert b is None
