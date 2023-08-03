"""new_course_window.py"""

from pathlib import Path
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class NewCourseWindow(QDialog):
    """A window that allows the user to create a new course"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).parents[0] / "new_course_window.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())

        self.clear_fields_button.clicked.connect(self.clear_fields)
        self.language_entry.textChanged.connect(self.course_name_changed)
        self.name_entry.textChanged.connect(self.course_language_changed)

        self.ok_button.clicked.connect(self.submit_inputs)
        self.cancel_button.clicked.connect(self.close_window)

    def clear_fields(self):
        """Clears the lineEdit fields of the course name and language"""
        self.name_entry.setText("")
        self.language_entry.setText("")
    
    def close_window(self):
        """Closes the window"""
        self.close()

    def submit_inputs(self):
        """Submits and stores the course information"""
        pass

    def check_valid_inputs(self) -> bool:
        """Checks that the course name and language are valid and new"""
        # Check there is text in both fields
        # Check that the supplied name does not already exist
        # Submit a bool

    def course_name_changed(self):
        pass

    def course_language_changed(self):
        pass
