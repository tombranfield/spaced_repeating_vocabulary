"""courses_dao_2.py"""


from collections import namedtuple
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
#    COURSES_PATH = str(Path(__file__).parents[2] / "data" / "courses.db")

    def __init__(self, db_path=Database.path):
        """Initializes the database."""
        self.db = Database(db_path)
        self._create_courses_table()

    def add_new_course(self, course_name, course_language):
        """Creates a new course"""
        if self._does_course_already_exist(course_name):
            raise DuplicateEntryException
        else:
            query = (
                "INSERT INTO " + self.COURSES_TABLE_NAME + " ("
                + "course_name, course_language) VALUES( "
                + "\'" + course_name + "\', "
                + "\'" + course_language + "\')"
            )
            self.db.connect_and_execute(query)

    def delete_course(self, course_name):
        """Deletes a course and all of its words"""
        query = (
            "DELETE FROM " + self.COURSES_TABLE_NAME + " where course_name "
            + " = \'" + course_name + "\'"
        )
        self.db.connect_and_execute(query)
        word_list_dao = WordListDAO()
        word_list_dao.delete_word_list(course_name)

    def courses_list(self):
        """Returns a list of courses"""
        query = "SELECT DISTINCT course_name FROM " + self.COURSES_TABLE_NAME
        result = self.db.result_from_query(query)
        courses = []
        if result:
            for course in result:
                courses.append(course[0])
        return courses

    def language(self, course_name):
        """Returns the language of the course"""
        query = (
            "SELECT course_language FROM " + self.COURSES_TABLE_NAME
            + " WHERE course_name = \'" + course_name + "\'"
        )
        result = self.db.result_from_query(query)
        if result:
            return result[0][0]

    def course_words(self, course_name):
        """Returns the words of the course"""
        course_words = {}
        course_word = namedtuple("id", ["foreign_word", "translated_word", "is_known", "when_review"])
        query = (
            "SELECT rowid, foreign_word, translated_word, is_known, "
            + "when_review FROM " + Database.table_name + " WHERE "
            + "word_list_name = \'" + course_name + "\'"
        )
        result = self.db.result_from_query(query)
        for entry in result:
            id = entry[0]
            for_word = entry[1]
            trans_word = entry[2]
            is_known = entry[3]
            when_review = entry[4]
            row = [id, for_word, trans_word, is_known, when_review]
            course_words[id] = course_word(for_word, trans_word, is_known, when_review)
        print(len(course_words))
        return course_words
            

    def _does_course_already_exist(self, course_name) -> bool:
        """Returns whether the course already exists"""
        query = (
            "SELECT COUNT() FROM " + self.COURSES_TABLE_NAME
            + " WHERE course_name = \'" + course_name + "\'"
        )
        count = self.db.result_from_query(query)[0][0]
        if count > 0:
            return True
        return False

    def _create_courses_table(self):
        """Creates a new courses table, if it doesn't exist"""
        query = (
            "CREATE TABLE IF NOT EXISTS " + self.COURSES_TABLE_NAME
            + "(course_name TEXT, course_language TEXT);"
        )
        self.db.connect_and_execute(query)
            


if __name__ == "__main__":
    courses_dao = CoursesDAO()

    print(courses_dao.courses_list())

    print(courses_dao.course_words("My Newest List"))
