"""
Testing row_dao.py
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.row import Row
from src.database.row_dao import RowDAO


@pytest.fixture
def row_dao():
    with TemporaryDirectory() as tmp_dir:
        db_name = "temp_testing_db.db"
        db_path = str(Path(tmp_dir)) + db_name
        row_dao = RowDAO(db_path)
        yield row_dao


@pytest.fixture
def row_dao_one_row_db(row_dao, row_of_data):
    row_dao.insert_row(row_of_data)
    yield row_dao


def test_row_dao_creates_db(row_dao):
    num_rows = row_dao.total_rows()
    assert num_rows == 0


def test_row_dao_inserts_row_successfully(row_dao, row_of_data):
    num_rows_before = row_dao.total_rows()
    row_dao.insert_row(row_of_data)
    num_rows_after = row_dao.total_rows()
    assert num_rows_before == 0 and num_rows_after == 1


def test_row_insert_row_inserts_correct_data(row_dao, row_of_data):
    row_dao.insert_row(row_of_data)    
    for_word = row_of_data.foreign_word
    list_name = row_of_data.word_list_name

    out_foreign_word = row_dao._column_value("foreign_word", for_word, list_name)
    out_trans_word = row_dao._column_value("translated_word", for_word, list_name)
    out_language = row_dao._column_value("language", for_word, list_name)
    out_list_name = row_dao._column_value("word_list_name", for_word, list_name)

    assert out_foreign_word == row_of_data.foreign_word
    assert out_trans_word == row_of_data.translated_word
    assert out_language == row_of_data.language
    assert out_list_name == row_of_data.word_list_name


def test_row_dao_correct_default_values_on_insertion(row_dao, row_of_data):
    row_dao.insert_row(row_of_data)
    for_word = row_of_data.foreign_word
    list_name = row_of_data.word_list_name

    level = row_dao._column_value("level", for_word, list_name)
    num_correct = row_dao._column_value("num_correct", for_word, list_name)
    num_incorrect = row_dao._column_value("num_incorrect", for_word, list_name)
    is_known = row_dao._column_value("is_known", for_word, list_name)
    is_review = row_dao._column_value("is_review", for_word, list_name)
 
    assert (level == num_correct == num_incorrect == is_known
            == is_review == 0)


def test_inserts_multiple_row_in_succession(row_dao, rows_of_data):
    num_rows_before = row_dao.total_rows()
    for row in rows_of_data:
        row_dao.insert_row(row)
    num_rows_after = row_dao.total_rows()
    assert num_rows_before == 0 and num_rows_after == 3


def test_row_dao_one_row_db(row_dao_one_row_db):
    num_rows = row_dao_one_row_db.total_rows()
    assert num_rows == 1


def test_is_word_already_there(row_dao_one_row_db, row_of_data):
    foreign_word = row_of_data.foreign_word
    word_list_name = row_of_data.word_list_name
    assert row_dao_one_row_db.is_word_already_there(foreign_word, word_list_name) == True


def test_is_word_not_there(row_dao_one_row_db, row_of_data):
    foreign_word = "random nonsense string"
    word_list_name = "randomstuffandnonsense"
    assert row_dao_one_row_db.is_word_already_there(foreign_word, word_list_name) == False


def test_word_is_there_but_in_different_list(row_dao_one_row_db, row_of_data):
    foreign_word = row_of_data.foreign_word
    other_list = "Other List Name Completely Different"
    assert row_dao_one_row_db.is_word_already_there(foreign_word, other_list) == False


# TODO How do you know to use row_of_data on one_row_db
def test_delete_row(row_dao_one_row_db, row_of_data):
    num_rows_before = row_dao_one_row_db.total_rows()
    row_dao_one_row_db.delete_row(row_of_data.foreign_word,
                                  row_of_data.word_list_name)
    num_rows_after = row_dao_one_row_db.total_rows()
    assert num_rows_before == 1 and num_rows_after == 0


def test_delete_row_when_list_doesnt_exist(row_dao_one_row_db, row_of_data):
    row_dao_one_row_db.delete_row(row_of_data.foreign_word,
                                     "non-existent list") 
    assert row_dao_one_row_db.total_rows() == 1


def test_delete_row_when_word_doesnt_exist(row_dao_one_row_db, row_of_data):
    row_dao_one_row_db.delete_row("non-existent word", 
                                   row_of_data.word_list_name) 
    assert row_dao_one_row_db.total_rows() == 1




def test_format_rows(row_dao, rows_of_data):
    formatted_rows = row_dao._format_rows(rows_of_data)
    print(formatted_rows)
    assert isinstance(formatted_rows, list)
    assert len(formatted_rows) == 3
    assert formatted_rows[0] == ("basic words", "bonjour", "hello", "french")
    assert formatted_rows[1] == ("basic words", "merci", "thank you", "french")
    assert formatted_rows[2] == ("basic words", "au revoir", "goodbye", "french")


def test_insert_rows(row_dao, rows_of_data):
    num_rows_before = row_dao.total_rows()
    row_dao.insert_rows(rows_of_data)
    num_rows_after = row_dao.total_rows()


def test_cannot_insert_duplicate_data(row_dao, row_of_data):
    row_dao.insert_row(row_of_data)
