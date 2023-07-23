"""
Represents the database for the Spaced Repeating Vocabulary program.
It holds the words, their translations, and other related information.
"""

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
    _DB_PATH = str(Path("wordlists.db"))
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

    def connect_and_execute(self, query: str):
        """
        Connects to the database, executes the supplied query,
        then closes the connection.
        """
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def result_from_query(self, query: str):
        """Returns a tuple result after query to the database"""
        connection = sqlite3.connect(self._db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        cursor.close()
        connection.close()
        return record

    # Takes up too much room - flatten it
    def _create_new_table(self):
        """Creates a new database, if it doesn't already exist."""
        create_table_query = "CREATE TABLE IF NOT EXISTS " + self.table_name + """ (
                                id INTEGER PRIMARY KEY,
                                word_list_name TEXT NOT NULL, 
                                foreign_word TEXT NOT NULL,
                                translated_word TEXT NOT NULL,
                                language TEXT NOT NULL,      
                                level INTEGER NOT NULL,
                                last_learnt_datetime DATETIME,
                                when_review DATETIME, 
                                num_correct INTEGER NOT NULL,
                                num_incorrect INTEGER NOT NULL,
                                is_known INTEGER NOT NULL,
                                is_review INTEGER NOT NULL);"""
        self.connect_and_execute(create_table_query)
        print("SQLite table", self._db_path, "created.")

   
    def total_rows(self):
        """        
        Returns the total number of words in the entire database
        from all word lists.
        """
        total_rows_query = "SELECT COUNT(*) FROM " + self.table_name
        query_result = self.result_from_query(total_rows_query)        
        return int(query_result[0][0])


if __name__ == "__main__":
    db = Database()

    print("Path:", Database.path)
    print("Table name:", Database.table_name)
