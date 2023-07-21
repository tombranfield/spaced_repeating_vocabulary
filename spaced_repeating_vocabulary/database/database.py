"""
Represents the database for the Spaced Repeating Vocabulary program.
It holds the words, their translations, and other related information.
"""

import sqlite3
import pathlib
import os.path


class Database:
    """
    Responsible for storing and handling the repository of
    words with their corresponding translations and other related 
    information.
    """
    # Goes in data folder which is up ../../data/
    # For now I will put it into the same folder as this module
    DB_PATH = "wordlists.db"
        
    def __init__(self):
        """Initializes the database."""
        self._db_filename = self.DB_PATH
        self._create_new_table()

    def connect_and_execute(self, query: str):
        """
        Connects to the database, executes the supplied query,
        then closes the connection.
        """
        connection = sqlite3.connect(self._db_filename)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    def _create_new_table(self):
        """Creates a new database, if it doesn't already exist."""
        create_table_query = """CREATE TABLE master_wordlist (
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
        self.connect_and_execute(create_table_query)
        print("SQLite table", self._db_filename, "created.")


if __name__ == "__main__":
    # Quick tests here... don't forget to pytest.

    db = Database()
