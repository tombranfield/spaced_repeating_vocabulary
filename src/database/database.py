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


    # TODO have an internal create query method?
    # Test that this works!
    # Takes up too much room - flatten it
    def _create_new_table(self):
        """Creates a new database, if it doesn't already exist."""
        create_table_query = "CREATE TABLE IF NOT EXISTS " + self.table_name + """ (
                                id INTEGER PRIMARY KEY,
                                list_name TEXT NOT NULL, 
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

    # TODO a list flag would be useful
    # be default, search the whole db
    # but with a flag, searches with only that list
    def total_rows(self):
        """
        Returns the total number of words in the entire database
        from all word lists.
        """
        total_rows_query = "SELECT COUNT(*) FROM " + self.table_name
        query_result = self.result_from_query(total_rows_query)        
        return int(query_result[0][0])


    def _create_insert_query(self, row):
        """
        Creates a query string that will be used to insert words into the
        database.
        """
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insert_query = ("INSERT INTO " + self.table_name + " (list_name," 
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
        # OK how to insert into a database?
        insert_query = self._create_insert_query(row)
        self.connect_and_execute(insert_query)


if __name__ == "__main__":
    # Quick tests here... don't forget to pytest.

    """
    db = Database()
    print("Total words:", db.total_rows())

    foreign_word = "bullig"
    translated_word = "cheap"
    foreign_language = "german"
    word_list_name = "Harry Potter und der Stein der Weisen"

    new_row = Row(foreign_word, translated_word, foreign_language,
                  word_list_name)

    db.insert_row(new_row)

    print("Path:",db.path)
    print("Table name:", db.table_name)
    """
    print("Class path:", Database.path)
    print("Class table name:", Database.table_name)
