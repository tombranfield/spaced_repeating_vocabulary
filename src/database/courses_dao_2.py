"""courses_dao.py"""


import os
from pathlib import Path

from src.database.database import Database
from src.database.exception import DuplicateEntryException
from src.database.word_list_dao import WordListDAO


class CoursesDAO:
    """
    Responsible for storing and retrieving the list of courses
    """
    COURSES_TABLE_NAME = "COURSES" 

    def __init__(self, db_path=Database.path):
        """Initializes the database."""
        self.db = Database(db_path)

    def add_new_course(self, course_name, course_language):
        """Creates a new course"""
        if self._does_course_already_exist(course_name):
            raise DuplicateEntryException
        else:
            # Add to COURSES_TABLE_NAME

    def delete_course(self, course_name):
        """Deletes a course and all of its words"""
        # Delete course from the courses table
        # Then delete all words from the word list
        word_list_dao = WordListDAO()
        word_list_dao.delete_word_list(course_name)

    def courses_list(self):
        """Returns a list of courses"""
        # Return a list of all the courses in the database

    def language(self, course_name):
        """Returns the language of the course"""
        # Returns the language of the course
        # Use a query SELECT language WHERE course_name = course_name


    def _does_course_already_exist(self, new_course_name) -> bool:
        """Returns whether the course already exists"""
        # Query the database and see whether the course is already there


if __name__ == "__main__":
    course_name = "Harry Potter und der Stein der Weisen"
    language = "German"

    courses_dao = CoursesDAO()

    print(courses_dao.courses_list())

    courses_dao.delete_course("Harry Potter")
    courses_dao.delete_course("a")

    print(courses_dao.courses_list())

