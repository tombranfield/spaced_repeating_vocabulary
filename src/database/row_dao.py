"""
Responsible for database operations associated with rows such as insertion
or deletion.
"""

from datetime import datetime
from pathlib import Path
import sqlite3

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
        # Convert list or tuple of rows into a list of tuples
        # Need this format to use executemany for sqlite3

    def _format_rows(self, rows):
        """
        Converts a list or tuple of Rows into a list of tuples where each
        tuple contains the data of the row. This is necessary in order to use
        the executemany instruction in sqlite3.
        """
        row_list_for_executemany = []
        for row in rows:
            row_data_tuple = (row.foreign_word, row.translated_word,
                              row.language, row.word_list_name)
            row_list_for_executemany.append(row_data_tuple)





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





    # TODO Might be nice to supply a word_list_name, so you can get
    # the total number of words for that list
    # If not, may as well use the one in the database
    def total_rows(self):
        """
        Returns the total number of rows in the entire database from all word
        lists.
        """
        total_rows_query = "SELECT COUNT(*) FROM " + Database.table_name
        query_result = self.db.result_from_query(total_rows_query)
        return int(query_result[0][0])


    def _create_insert_query(self, row):
        """
        Creates a query string that will be used to insert words into the
        database.
        """
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert_query = ("INSERT INTO " + Database.table_name + " (word_list_name," 
                     + "foreign_word, translated_word, language, level, "
                     + "last_learnt_datetime, when_review, num_correct, "
                     + "num_incorrect, is_known, is_review) VALUES( "
                     + "\'" + row.word_list_name + "\', "
                     + "'" + row.foreign_word + "\',"
                     + "'" + row.translated_word + "\',"
                     + "'" + row.language + "\',"
                     + "0,"
                     + "'" + current_datetime + "\',"
                     + "'" + current_datetime + "\',"
                     + "0,0,0,0)")
        return insert_query




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

    row = Row(foreign_word, translated_word, language, word_list_name)

    my_dao.insert_row(row)

    my_dao.stuff()
