"""courses_dao.py"""


import os
from pathlib import Path

from src.database.exception import DuplicateEntryException
from src.database.word_list_dao import WordListDAO


class CoursesDAO:
    """
    Responsible for storing and retrieving the list of courses
    """
    COURSES_PATH = str(Path(__file__).parents[2] / "data" / "courses.dat")

    def __init__(self, courses_path=COURSES_PATH):
        """Initializes the database."""
        self.courses_path = courses_path

    def add_new_course(self, course_name, course_language):
        """Creates a new course"""
        if self._does_course_already_exist(course_name):
            raise DuplicateEntryException
        else:
            with open(self.courses_path, "a") as file_obj:
                line = course_name + "|" + course_language + "\n"
                file_obj.write(line)

    def delete_course(self, course_name):
        """Deletes a course and all of its words"""
        try:
            with open(self.courses_path, "r") as in_file:
                with open("temp.txt", "w") as out_file:
                    for line in in_file:
                        line = line.strip().split("|")
                        if line[0] != course_name:
                            line = "|".join(line) + "\n"
                            out_file.write(line)
            os.replace("temp.txt", self.courses_path)
        except FileNotFoundError:
            pass
        word_list_dao = WordListDAO()
        word_list_dao.delete_word_list(course_name)

    def courses_list(self):
        """Returns a list of courses"""
        courses = ()
        try:
            with open(self.courses_path, "r") as file_obj:
                for line in file_obj:
                    line = line.strip().split("|")
                    try:
                        courses += (line[0],)
                    except ValueError:
                        pass
        except FileNotFoundError:
            pass
        return courses

    def _does_course_already_exist(self, new_course_name) -> bool:
        """Returns whether the course already exists"""
        existing_courses = self.courses_list()
        if new_course_name in existing_courses:
                return True
        return False



if __name__ == "__main__":
    course_name = "Harry Potter und der Stein der Weisen"
    language = "German"

    courses_dao = CoursesDAO()

    print(courses_dao.courses_list())

    courses_dao.delete_course("Harry Potter")
    courses_dao.delete_course("a")

    print(courses_dao.courses_list())

