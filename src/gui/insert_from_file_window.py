"""insert_from_file_window.py"""


from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from src.database.exception import DuplicateEntryException


class InsertFromFileWindow(QDialog):
    """A window that allows the user to create a new course"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).parents[0] / "insert_from_file_window.ui"), self)
        self.setStyleSheet(open(str(Path("stylesheet.css"))).read())
        self.course_name = ""
        self.course_language = ""
        self.connect_widgets()

    def connect_widgets(self):
        """Connects widget signals and slots"""
        self.clear_fields_button.clicked.connect(self.clear_fields)
        self.clear_fields_button.setDefault(False)
        self.cancel_button.clicked.connect(self.close_window)
        self.name_entry.textChanged.connect(self.course_name_changed)
        self.language_entry.textChanged.connect(self.course_language_changed)
        self.browse_button.clicked.connect(self.browse_and_choose_file)

    def clear_fields(self):
        """Clears the lineEdit fields of the course name and language"""
        self.name_entry.setText("")
        self.language_entry.setText("")
    
    def close_window(self):
        """Closes the window"""
        self.close()

    def course_name_changed(self, lineEdit_field_string):
        """Sets the course name attribute to the contents of the lineEdit"""
        self.course_name = lineEdit_field_string

    def course_language_changed(self, lineEdit_field_string):
        """Sets the course name attribute to the contents of the lineEdit"""
        self.course_language = lineEdit_field_string

    def browse_and_choose_file(self):
        initial_dir = str(Path.home())
        filter = "Text files (*.txt)"
        filename = QFileDialog.getOpenFileName(
            self,
            directory=initial_dir,
            filter=filter)[0]
        filtered_filename_index = max(
            filename.rfind("/"), filename.rfind("\\")) + 1
        print(filename[filtered_filename_index:])
