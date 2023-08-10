"""delete_course_window.py"""


from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

from src.core.course import Course
from src.database.exception import DuplicateEntryException
from src.database.courses_dao import CoursesDAO


class DeleteCourseWindow(QDialog):
    """A window for the user to delete the course"""
    def __init__(self, course, parent=None):
        super(DeleteCourseWindow, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "delete_course_window.ui"), self)
#        self.setStyleSheet(open(str(Path("stylesheet.css"))).read())
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())
        self.courses_dao = CoursesDAO()
        self.course_name = course.name
        self.connect_widgets()

    def connect_widgets(self):
        """Connects widget signals and slots"""
        msg = "Are sure you want to delete \'" + self.course_name + "\'?"
        self.description_label.setText(msg)
        self.delete_button.clicked.connect(self.delete_course)
        self.cancel_button.clicked.connect(self.close_window)

    def delete_course(self):
        self.courses_dao.delete_course(self.course_name)
        self.close()

    def close_window(self):
        """Closes the window"""
        self.close()
