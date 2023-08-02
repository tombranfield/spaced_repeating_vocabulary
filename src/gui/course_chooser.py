"""course_chooser.py"""

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget

from about_window import AboutWindow
from settings_window import SettingsWindow


base_dir = os.path.dirname(__file__)


class CourseChooser(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(base_dir, "course_chooser.ui"), self)
        self.setStyleSheet(open(os.path.join(base_dir,"stylesheet.css")).read())

        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CourseChooser()
    window.show()
    app.exec_()
