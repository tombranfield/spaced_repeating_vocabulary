import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from src.core.settings import Settings


base_dir = os.path.dirname(__file__)


class SettingsWindow(QDialog):
    """A window for viewing and setting the program settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(base_dir, "settings_window.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())
        self.settings = Settings()

        # Connect the buttons to the functions

        self.set_defaults_button.clicked.connect(self.set_defaults)

        if self.settings.is_case_sensitive == True:
            print("it's true")
            self.is_case_sensitive_cbox.setCheckState(Qt.Checked)
        else:
            print("it's false")
            self.is_case_sensitive_cbox.setCheckState(Qt.Unchecked)
        self.is_case_sensitive_cbox.stateChanged.connect(self.case_sensitivity_changed)                

        # Set the initial values of the boxes etc to those in
        # settings

        #self.is_automatic_return_cbox

        #self.max_learn_words_box
        #self.max_review_words_box


    def set_defaults(self):
        print("setting defaults")
        self.settings.set_defaults()


    def case_sensitivity_changed(self):
        if self.is_case_sensitive_cbox.isChecked():
            self.settings.is_case_sensitive = True 
        else:
            self.settings.is_case_sensitive = False

    def automatic_return_changed(self, s):
        if self.is_automatic_return_cbox.isChecked():
            self.settings.is_automatic_return = True
        else:
            self.settings.is_automatic_return = False

    def num_learn_words_changed(self, s):
        self.settings.max_learn_words = int(s)

    def num_review_words_changed(self, s):
        self.settings.max_review_words = int(s)







