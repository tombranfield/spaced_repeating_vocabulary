"""temp_dialog.py"""

from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog


class TempDialog(QDialog):
    """A window that tells the user what the program is and how to use it"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).parents[0] / "about_window.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())
        self.ok_button.clicked.connect(self.close_window)       
        QTimer.singleShot(100, self.close) # 1 millisecond
    
    def close_window(self):
        self.close()

