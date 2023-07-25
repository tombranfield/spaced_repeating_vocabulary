"""
Represents the database for the Spaced Repeating Vocabulary program.
It holds the words, their translations, and other related information.
"""

from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
import sqlite3

from src.core.row import Row


class Database:
    """
    Responsible for storing and handling the repository of
    words with their corresponding translations and other related 
    information.
    """
    _DB_PATH = str(Path("allwords.db"))
    _TABLE_NAME = "MASTER_WORD_LIST"
        
    def __init__(self, db_path=_DB_PATH):
        """Initializes the database."""
        self._db_path = db_path
        self._create_new_table()

    @classmethod
    @property
    def path(cls):
        return cls._DB_PATH

    @classmethod
    @property
    def table_name(cls):
        return cls._TABLE_NAME

    @contextmanager
    def db_cursor(self):
        """Handles connecting and disconnecting from the db"""
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        yield cursor
        connection.commit()
        connection.close()

    def connect_and_execute(self, query: str):
        """
        Connects to the database, executes the supplied query,
        then closes the connection.
        """
        with self.db_cursor() as cursor:
            cursor.execute(query)

    def result_from_query(self, query: str):
        """Returns a tuple result after query to the database"""
        with self.db_cursor() as cursor:
            cursor.execute(query)
            record = cursor.fetchall()
        return record

    def _create_new_table(self):
        """Creates a new database, if it doesn't already exist."""
        query = "CREATE TABLE IF NOT EXISTS " + self.table_name + """ (
                 rowid INTEGER PRIMARY KEY,
                 word_list_name TEXT, 
                 foreign_word TEXT,
                 translated_word TEXT,
                 language TEXT,      
                 level INTEGER DEFAULT 0,
                 last_learnt_datetime DATETIME,
                 when_review DATETIME, 
                 num_correct INTEGER DEFAULT 0,
                 num_incorrect INTEGER DEFAULT 0,
                 is_known INTEGER DEFAULT 0,
                 is_review INTEGER DEFAULT 0);"""
        self.connect_and_execute(query)
   
    def total_rows(self):
        """        
        Returns the total number of words in the entire database
        from all word lists.
        """
        total_rows_query = "SELECT COUNT(*) FROM " + self.table_name
        query_result = self.result_from_query(total_rows_query)        
        return int(query_result[0][0])

    def read_columns(self, *args):
        """Reads the data from the supplied columns"""
        # Basically a generic read method. Use with other dao


if __name__ == "__main__":
    db = Database()

    print("Path:", Database.path)
    print("Table name:", Database.table_name)
