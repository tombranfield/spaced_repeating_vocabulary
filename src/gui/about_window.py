import os
import sys

from PyQt5 import QtWidgets, uic


base_dir = os.path.dirname(__file__)


class AboutWindow(QDialog):
    """A window that tells the user what the program is and how to use it"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(base_dir, "about_window.ui"), self)

    
    def close_window(self):
        self.close()

