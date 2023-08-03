"""course_dao.py"""

from pathlib import Path


class CourseDAO:
    """
    Responsible for storing and retrieving the list of courses
    """
    _COURSES_PATH = str(Path(__file__).parents[2] / "data" / "courses.dat")

    def __init__(self, courses_path=_COURSES_PATH):
        """Initializes the database."""
        self._courses_path = courses_path

    @classmethod
    @property
    def path(cls):
        return cls._COURSES_PATH




if __name__ == "__main__":
    pass
