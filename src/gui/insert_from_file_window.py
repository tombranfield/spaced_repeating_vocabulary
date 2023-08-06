"""insert_from_file_window.py"""


from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from src.database.exception import DuplicateEntryException


class InsertFromFileWindow(QDialog):
    """A window that allows the user to create a new course"""
    def __init__(self, course_name, parent=None):
        super(InsertFromFileWindow, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "insert_from_file_window.ui"), self)
        self.setStyleSheet(open(str(Path("stylesheet.css"))).read())
        self.course_name = course_name
        self.filename = ""
        self.connect_widgets()
        self.refresh_widgets()

    def connect_widgets(self):
        """Connects widget signals and slots"""
        msg = "Words for \'" + self.course_name + "\':"
        self.instructions_label.setText(msg)
        self.clear_fields_button.clicked.connect(self.clear_fields)
        self.clear_fields_button.setDefault(False)
        self.insert_button.clicked.connect(self.insert_file)
        self.cancel_button.clicked.connect(self.close_window)
        self.browse_button.clicked.connect(self.browse_and_choose_file)

    def clear_fields(self):
        """Clears the lineEdit fields of the course name and language"""
        self.filename = ""
        self.refresh_widgets()
    
    def refresh_widgets(self):
        # Refreshes is_valid_label, filename_label, and insert_button
        self.update_filename_label()
        self.update_insert_button()
    
    def update_insert_button(self):
        # If valid and has filename, then can insert
        can_insert = self.filename and self.is_valid_file()

    def is_valid_file(self):
        # file_dao = 
        pass

    def close_window(self):
        """Closes the window"""
        self.close()

    def browse_and_choose_file(self):
        """Opens a window so the user can choose the file to load"""
        initial_dir = str(Path.home())
        filter = "Text files (*.txt)"
        self.filename = QFileDialog.getOpenFileName(
            self,
            directory=initial_dir,
            filter=filter)[0]
        self.refresh_widgets()

    def update_filename_label(self):
        filtered_filename_index = max(
            self.filename.rfind("/"), self.filename.rfind("\\")) + 1
        filtered_filename = self.filename[filtered_filename_index:]
        self.selected_filename_label.setText(filtered_filename)

    def insert_file(self):
        # file_dao = FileDao()
        # is_valid = file_dao.is_valid(self.filename)
        # if not is_valid: messagebox
        # else:
        #       file_dao.insert_file(self.filename)

        pass            
