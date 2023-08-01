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


class TotalStats(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(base_dir, "total_stats_widget.ui"), self)
        self.setStyleSheet(open(os.path.join(base_dir,"stylesheet.css")).read())

        self.total_stats = TotalStats()
        self.setup_stats_update()

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
    
    def get_new_stats(self):
        self.total_stats.total_words_learnt()
        self.total_stats.total_words_to_review()
        self.total_stats.total_words()

    def add_labels_to_layout(self):
        pass




app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
