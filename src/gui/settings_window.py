import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

# TODO
# from src.core.settings import Settings


base_dir = os.path.dirname(__file__)


class SettingsWindow(QDialog):
    """A window for viewing and setting the program settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(base_dir, "settings_window.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())


    def num_learn_words_changed(self, s):
        self.settings.set_max_learn_words(int(s))


    def num_review_words_changed(self, s):
        self.settings.set_max_review_words(int(s))


    def set_defaults(self):
        pass


#    self.settings = Settings()

"""
    self.set_defaults_button
    
    self.is_case_sensitive_cbox
    self.is_automatic_return_cbox

    self.max_learn_words_box
    self.max_review_words_box
"""

