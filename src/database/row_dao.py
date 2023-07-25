"""
Responsible for database operations associated with rows such as insertion
or deletion.
"""

from datetime import datetime

from src.database.database import Database
from src.core.row import Row


class RowDAO:
    """
    Acts as an interface to the database in order to perform
    operations on rows such as insertion or deletion.
    """
    def __init__(self, db_path=Database.path):
        """Initializes the row data access object"""
        self.db = Database(db_path)

    def insert_row(self, row):
        """Inserts an individual row into the database"""
        insert_query = self._create_insert_query(row)
        self.db.connect_and_execute(insert_query)
        
    def insert_rows(self, rows):
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

    def delete_row(self, foreign_word):
        """
        Deletes the row containing the supplied foreign word from the database.
        """
        query = ("DELETE FROM " + Database.table_name + " where "
                 "foreign_word = \'" + foreign_word + "\'")
        self.db.connect_and_execute(query)

    def delete_rows_of_word_list(self, word_list_name):
        """Deletes all the rows associated with the supplied word list"""
        query = ("DELETE FROM " + Database.table_name + " where "
                 "word_list_name = \'" + word_list_name + "\'")
        self.db.connect_and_execute(query)

    # This might not be necessary, since have separate list_dao now
    def total_rows(self):
        """
        Returns the total number of rows in the entire database from all word
        lists.
        """
        total_rows_query = "SELECT COUNT(*) FROM " + Database.table_name
        query_result = self.db.result_from_query(total_rows_query)
        return int(query_result[0][0])


    def _multiple_insert_query(self):
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert_query = ("INSERT INTO " + Database.table_name + " ("
                     + "word_list_name, foreign_word, translated_word, "
                     + "language, last_learnt_datetime, when_review) "
                     + "VALUES(?, ?, ?, ?,"
                     + "'" + current_datetime + "\',"
                     + "'" + current_datetime + "\')")
        return insert_query


    def _create_insert_query(self, row):
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert_query = ("INSERT INTO " + Database.table_name + " ("
                     + "word_list_name, foreign_word, translated_word, "
                     + "language, last_learnt_datetime, when_review) "
                     + "VALUES( "
                     + "\'" + row.word_list_name + "\', "
                     + "'" + row.foreign_word + "\',"
                     + "'" + row.translated_word + "\',"
                     + "'" + row.language + "\',"
                     + "'" + current_datetime + "\',"
                     + "'" + current_datetime + "\')")
        return insert_query


    # Add a list as parameter so can have same word in different lists
    def is_word_already_there(self, foreign_word):
        """Looks in the database to see if the foreign word is already in it"""
        query = ("SELECT(EXISTS(SELECT foreign_word FROM " + Database.table_name
              + " where foreign_word = '" + foreign_word + "\'))")
        query_result = self.db.result_from_query(query)
        return query_result[0][0]


if __name__ == "__main__":

    my_dao = RowDAO()

    foreign_word = "bullig"
    translated_word = "cheap"
    language = "german"
    word_list_name = "Harry Potter und der Stein"

    row1 = Row(foreign_word, translated_word, language, word_list_name)
    row2 = Row("foreign", "trans", "lang", "list_name")
    row3 = Row("A", "B", "C", "D")
    rows = (row1, row2, row3)

    my_dao.insert_rows(rows)

    print(my_dao.get_id("foreign", "list_name"))
    print(my_dao.get_id(foreign_word, word_list_name))
