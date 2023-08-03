"""course_dao.py"""

from pathlib import Path


class CourseDAO:
    """
    Responsible for storing and retrieving the list of courses
    """
    COURSES_PATH = str(Path(__file__).parents[2] / "data" / "courses.dat")

    def __init__(self, courses_path=COURSES_PATH):
        """Initializes the database."""
        self.courses_path = courses_path

    def add_new_course(self, course_name, course_language):
        """Creates a new course"""
        with open(self.courses_path, "w") as file_obj:
            line = course_name + "|" + course_language
            file_obj.write(line)

    def courses_list(self):
        """Returns a list of courses"""
        pass

    def does_course_already_exist(self, course_name) -> bool:
        """Returns whether the course already exists"""
        pass



if __name__ == "__main__":
    course_name = "Harry Potter und der Stein der Weisen"
    language = "German"

    course_dao = CourseDAO()

    course_dao.add_new_course(course_name, language)
