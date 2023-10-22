"""browse_course_window.py"""


from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

from src.core.course import Course
from src.database.courses_dao import CoursesDAO


class BrowseCourseWindow(QDialog):
    """A window for the user to delete the course"""
    def __init__(self, course, parent=None):
        super(BrowseCourseWindow, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "browse_course_window.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())
        self.courses_dao = CoursesDAO()
        self.course_name = course.name
        self.connect_widgets()

    def connect_widgets(self):
        """Connects widget signals and slots"""
        self.close_button.clicked.connect(self.close_window)

    def close_window(self):
        """Closes the window"""
        self.close()
