"""new_course_window.py"""

import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


base_dir = os.path.dirname(__file__)


class NewCourseWindow(QDialog):
    """A window that allows the user to create a new course"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(base_dir, "new_course_window.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())

        self.cancel_button.clicked.connect(self.close_window)
        self.ok_button.clicked.connect(self.close_window)
        
    
    def close_window(self):
        self.close()

