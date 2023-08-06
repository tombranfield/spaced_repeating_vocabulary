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
        self.filename = ""
        self.connect_widgets()

    def connect_widgets(self):
        """Connects widget signals and slots"""
        self.clear_fields_button.clicked.connect(self.clear_fields)
        self.clear_fields_button.setDefault(False)
        self.cancel_button.clicked.connect(self.close_window)
        self.browse_button.clicked.connect(self.browse_and_choose_file)

    def clear_fields(self):
        """Clears the lineEdit fields of the course name and language"""
        self.filename = ""
        self.set_filename_label()
    
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
        self.set_filename_label()

    def set_filename_label(self):
        filtered_filename_index = max(
            self.filename.rfind("/"), self.filename.rfind("\\")) + 1
        filtered_filename = self.filename[filtered_filename_index:]
        self.selected_filename_label.setText(filtered_filename)
        

        # We use filtered filename for the display
        # We use the raw filename for opening the file
