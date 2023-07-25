"""
Responsible for database operations associated with word lists such as insertion
or deletion.
"""

from datetime import datetime

from src.database.database import Database
from src.core.row import Row
from src.core.word_list import WordList


class WordListDAO:
    """
    Acts as an interface to the database in order to perform
    operations on rows such as insertion or deletion.
    """
    def __init__(self, db_path=Database.path):
        """Initializes the row data access object"""
        self.db = Database(db_path)

    def insert_word_list(self, word_list: WordList):
        """Inserts a word list into the database"""     
        # Check is a valid word list
        # Check there are no duplicates in the database
        rows = self._create_rows(word_list)
        self._insert_rows(rows)

    def delete_word_list(self, word_list_name):
        """Deletes all the rows associated with the supplied word list"""
        query = ("DELETE FROM " + Database.table_name + " where "
                 "word_list_name = \'" + word_list_name + "\'")
        self.db.connect_and_execute(query)

    def _create_rows(self, word_list: WordList):
        """Returns a list of Rows from the supplied WordList instance"""
        rows = []
        language = word_list.language
        word_list_name = word_list.name
        For word_pair in word_list.word_pairs:
            row = Row(word_pair.foreign_word, word_pair.translated_word,
                      language, word_list_name)
            rows.append(row)
        return rows


    def _insert_rows(self, rows: Row):
        """Inserts rows into the database"""
        formatted_rows = self._format_rows(rows)
        query = self._multiple_insert_query()
        with self.db.db_cursor() as cursor:
            cursor.executemany(query, formatted_rows)


    def _format_rows(self, rows):
        """
        Converts a list or tuple of Rows into a list of tuples where each
        tuple contains the data of the row. This is necessary in order to use
        the executemany instruction in sqlite3.
        """
        row_list_for_executemany = []
        for row in rows:
            row_data_tuple = (row.word_list_name, row.foreign_word, 
                              row.translated_word, row.language)
            row_list_for_executemany.append(row_data_tuple)
        return row_list_for_executemany


    def _multiple_insert_query(self):
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert_query = ("INSERT INTO " + Database.table_name + " ("
                     + "word_list_name, foreign_word, translated_word, "
                     + "language, last_learnt_datetime, when_review) "
                     + "VALUES(?, ?, ?, ?,"
                     + "'" + current_datetime + "\',"
                     + "'" + current_datetime + "\')")
        return insert_query

    def is_word_already_there(self, foreign_word, word_list_name):
        """Looks in the database to see if the foreign word is already in it"""
        query = ("SELECT(EXISTS(SELECT foreign_word FROM " + Database.table_name
              + " where foreign_word == \'" + foreign_word + "\' AND"
              + " word_list_name == \'" + word_list_name + "\'))")
        query_result = self.db.result_from_query(query)
        return query_result[0][0]

    def _column_value(self, column_name, foreign_word, word_list_name):
        """
        Gets the supplied value in the given column for the supplied word 
        in the word list
        """
        conditions = {"foreign_word": foreign_word, "word_list_name": word_list_name}
        value = self.db.read_cell(column_name, **conditions)
        return value


if __name__ == "__main__":

    my_dao = RowDAO()

    foreign_word = "bullig"
    translated_word = "cheap"
    language = "german"
    word_list_name = "Harry Potter und der Stein"

    row1 = Row(foreign_word, translated_word, language, word_list_name)
    """
    row2 = Row("foreign", "trans", "lang", "list_name")
    row3 = Row("A", "B", "C", "D")
    rows = (row1, row2, row3)
   
    my_dao.insert_rows(rows)
    """

    my_dao.insert_row(row1)
    print(my_dao.is_word_already_there(foreign_word, word_list_name))
    print(my_dao.is_word_already_there("randomwordstring", "fartbook"))

