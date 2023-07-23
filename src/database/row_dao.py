"""
insertion_dao.py

Data Access Object responsible for inserting into the database
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
    # Get the DB path and table name from the database
    def __init__(self, db_path=DB_PATH):
        """Initializes the database."""
        self.db = database.Database(db_path)

    def _create_insert_query(self, row):
        """
        Creates a query string that will be used to insert words into the
        database.
        """
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert_query = ("INSERT INTO " + self.TABLE_NAME + " (list_name," 
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

        
    # TODO Equivalent to insert_individual in old program
    def insert_row(self, row):
        """Inserts an individual word into the database"""
        insert_query = self._create_insert_query(row)
        self.db.connect_and_execute(insert_query)

    def stuff(self):
        print("waddup")


if __name__ == "__main__":

    my_dao = InsertionDAO()
    my_dao.stuff
