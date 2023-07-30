import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


base_dir = os.path.dirname(__file__)


class SettingsWindow(QDialog):
    """A window for viewing and setting the program settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(base_dir, "settings_window.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())

        self.ok_button.clicked.connect(self.close_window)
        
    
    def close_window(self):
        self.close()

