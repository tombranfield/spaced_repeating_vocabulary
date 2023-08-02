"""header.py"""

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QWidget

from about_window import AboutWindow
from settings_window import SettingsWindow


base_dir = os.path.dirname(__file__)


class Header(QWidget):
    def __init__(self):
        """Header class which holds the about and settings buttons"""
        super().__init__()
        uic.loadUi(os.path.join(base_dir, "header.ui"), self)
        self.setStyleSheet(open(os.path.join(base_dir,"stylesheet.css")).read())

        # self.new_course_button.clicked.connect(self.new_course_window)
        self.about_button.clicked.connect(self.open_about_window)
        self.settings_button.clicked.connect(self.open_settings_window)


    def open_about_window(self):
        dialog = AboutWindow(self)
        dialog.exec_()

    def open_settings_window(self):
        dialog = SettingsWindow(self)
        dialog.exec_()

    """
    def new_about_window(self):
        dialog = NewCourseWindow(self)
        dialog.exec_()
    """



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Header()
    window.show()
    app.exec_()
