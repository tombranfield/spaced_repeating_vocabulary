"""main_window.py"""

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog

from about_window import AboutWindow
from settings_window import SettingsWindow
from src.core.total_stats import TotalStats


base_dir = os.path.dirname(__file__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(base_dir, "mainwindow.ui"), self)
        self.setStyleSheet(open(os.path.join(base_dir,"stylesheet.css")).read())

        self.setup_stats_update()

        self.about_button.clicked.connect(self.open_about_window)
        self.settings_button.clicked.connect(self.open_settings_window)


    def open_about_window(self):
        dialog = AboutWindow(self)
        dialog.exec_()

    def open_settings_window(self):
        dialog = SettingsWindow(self)
        dialog.exec_()






app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
