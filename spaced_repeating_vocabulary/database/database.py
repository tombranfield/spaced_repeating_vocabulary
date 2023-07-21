"""
Represents the database for the Spaced Repeating Vocabulary program.
It holds the words, their translations, and other related information.
"""

import sqlite3
import pathlib
import os.path


def connect_to_db(func):
    def wrapper():
        # do before stuff
        func()
        # do after stuff
    return wrapper



class Database:
    """
    Responsible for storing and handling the repository of
    words and their translatations and other related information.
    """
    # Goes in data folder which is up ../../data/
    # For now I will put it into the same folder as this module
    DB_PATH = "wordlists.db"
        
    def __init__(self):
        """Initializes the database."""
        self._db_filename = self.DB_PATH
        self._create_new_table()

    def _create_new_table(self):
        """Creates a new database, if it doesn't already exist."""
        connection = sqlite3.connect(self._db_filename)
        cursor = connection.cursor()
        CREATE_TABLE_STRING = """CREATE TABLE master_wordlist (
                                  id INTEGER PRIMARY KEY,
                                  list_name TEXT NOT NULL, 
                                  foreign_word TEXT NOT NULL,
                                  translated_word TEXT NOT NULL,
                                  language TEXT NOT NULL,      
                                  level INTEGER NOT NULL,
                                  learnt_datetime DATETIME,
                                  when_review DATETIME, 
                                  num_correct INTEGER NOT NULL,
                                  num_incorrect INTEGER NOT NULL,
                                  is_known INTEGER NOT NULL,
                                  is_review INTEGER NOT NULL);"""
        create_table_query = CREATE_TABLE_STRING
        cursor.execute(create_table_query)
        connection.commit()
        print("SQLite table", self._db_filename, "created.")
        cursor.close()
        connection.close()


if __name__ == "__main__":
    # Quick tests here... don't forget to pytest.

    db = Database()
