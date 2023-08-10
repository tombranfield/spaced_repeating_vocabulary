"""new_course_window.py"""


from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

from src.database.exception import DuplicateEntryException
from src.database.courses_dao import CoursesDAO


class NewCourseWindow(QDialog):
    """A window that allows the user to create a new course"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).parents[0] / "new_course_window.ui"), self)
#        self.setStyleSheet(open(str(Path("stylesheet.css"))).read())
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())
        self.courses_dao = CoursesDAO()
        self.connect_widgets()
        self.course_name = ""
        self.course_language = ""
        self.update_ok_button()

    def connect_widgets(self):
        """Connects widget signals and slots"""
        self.clear_fields_button.clicked.connect(self.clear_fields)
        self.clear_fields_button.setDefault(False)
        self.name_entry.textChanged.connect(self.course_name_changed)
        self.language_entry.textChanged.connect(self.course_language_changed)
        self.ok_button.clicked.connect(self.add_new_course)
        self.ok_button.setDefault(True)
        self.cancel_button.clicked.connect(self.close_window)

    def clear_fields(self):
        """Clears the lineEdit fields of the course name and language"""
        self.name_entry.setText("")
        self.language_entry.setText("")
    
    def close_window(self):
        """Closes the window"""
        self.close()

    def add_new_course(self):
        """Submits and stores the course information"""
        try:
            self.courses_dao.add_new_course(self.course_name, 
                                            self.course_language)
            self.close()
        except DuplicateEntryException:
            msg = "That course already exists."
            self.new_course_message_label.setText(msg)

    def course_name_changed(self, lineEdit_field_string):
        """Sets the course name attribute to the contents of the lineEdit"""
        self.course_name = lineEdit_field_string
        self.update_ok_button()
        self.new_course_message_label.setText("")

    def course_language_changed(self, lineEdit_field_string):
        """Sets the course name attribute to the contents of the lineEdit"""
        self.course_language = lineEdit_field_string
        self.update_ok_button()

    def update_ok_button(self):
        if self.course_name and self.course_language:
            self.ok_button.setEnabled(True)
            self.ok_button.setStyleSheet("background: lime")
        else:
            self.ok_button.setEnabled(False)
            self.ok_button.setStyleSheet("background: gray")
