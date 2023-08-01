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

        self.setup_defaults_button()
        self.setup_is_case_sensitive_box()
        self.setup_is_automatic_return_box()
        self.setup_max_learn_words_box()
        self.setup_max_review_words_box()

    def setup_defaults_button(self):
        self.set_defaults_button.clicked.connect(self.set_defaults)

    def set_defaults(self):
        self.settings.set_defaults()

    def setup_is_case_sensitive_box(self):
        if self.settings.is_case_sensitive == True:
            self.is_case_sensitive_cbox.setCheckState(Qt.Checked)
        else:
            self.is_case_sensitive_cbox.setCheckState(Qt.Unchecked)
        self.is_case_sensitive_cbox.stateChanged.connect(self.case_sensitivity_changed)

    def case_sensitivity_changed(self):
        if self.is_case_sensitive_cbox.isChecked():
            self.settings.is_case_sensitive = True 
        else:
            self.settings.is_case_sensitive = False

    def setup_is_automatic_return_box(self):
        if self.settings.is_automatic_return == True:
            self.is_automatic_return_cbox.setCheckState(Qt.Checked)
        else:
            self.is_automatic_return_cbox.setCheckState(Qt.Unchecked)
        self.is_automatic_return_cbox.stateChanged.connect(self.automatic_return_changed)

    def automatic_return_changed(self, s):
        if self.is_automatic_return_cbox.isChecked():
            self.settings.is_automatic_return = True
        else:
            self.settings.is_automatic_return = False

    def setup_max_learn_words_box(self):
        self.max_learn_words_cbox.setCurrentText(str(self.settings.max_learn_words))
        self.max_learn_words_cbox.currentIndexChanged[str].connect(self.max_learn_words_changed)

    def max_learn_words_changed(self, s):
        self.settings.max_learn_words = int(s)

    def setup_max_review_words_box(self):
        self.max_review_words_cbox.setCurrentText(str(self.settings.max_review_words))
        self.max_review_words_cbox.currentIndexChanged[str].connect(self.max_review_words_changed)

    def max_review_words_changed(self, s):
        self.settings.max_review_words = int(s)
