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
        #self.review_all_button.clicked.connect()


#    total_learn_label
#    total_review_label


    def open_about_window(self):
        dialog = AboutWindow(self)
        dialog.exec_()

    def open_settings_window(self):
        dialog = SettingsWindow(self)
        dialog.exec_()

    def setup_stats_update(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_stats_display)
        self.timer.start()

    def update_stats_display(self):
        self.remove_labels()
        self.get_new_stats()
        self.get_new_labels()
        self.add_labels_to_layout()

    def remove_labels(self):
        self.remove_widget(self.total_learnt_label)
        self.remove_widget(self.total_review_label)
    





app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
