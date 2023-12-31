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
#    _DB_PATH = str(Path("InformalWordList.db"))
    _DB_PATH = str(Path(__file__).parents[2] / "data" / "words.db")

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
                 level INTEGER DEFAULT 1,
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
        query = "SELECT COUNT(*) FROM " + self.table_name
        result = self.result_from_query(query)        
        return int(result[0][0])

    def read_cell(self, column_name, **kwargs):
        """Gets the desired column of the row given the supplied conditions"""
        query = "SELECT " + column_name + " FROM " + self.table_name + " WHERE "
        for column_name, value in kwargs.items():
            query += column_name + " == \'" + value + "\' AND "
        query = query[:-5]
        result = self.result_from_query(query)
        return result[0][0]


if __name__ == "__main__":
    db = Database()

    my_dict = {"foreign_word": "bullig", "translated_word": "cheap"}

    print(db.read_cell("rowid", **my_dict))
