"""
Represents the database for the Spaced Repeating Vocabulary program.
It holds the words, their translations, and other related information.
"""

import sqlite3
from pathlib import Path


class Database:
    """
    Responsible for storing and handling the repository of
    words with their corresponding translations and other related 
    information.
    """
#    DB_PATH = str(Path("../../data/wordlists.db"))
    DB_PATH = str(Path("wordlists.db"))
        
    def __init__(self, db_path=DB_PATH):
        """Initializes the database."""
        self._db_path = db_path
        self._create_new_table()

    def _connect_and_execute(self, query: str):
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

    # TODO have an internal create query method?
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
        self._connect_and_execute(create_table_query)
        print("SQLite table", self._db_path, "created.")


if __name__ == "__main__":
    # Quick tests here... don't forget to pytest.

    db = Database("test_db.db")
