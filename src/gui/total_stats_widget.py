"""total_stats_widget.py"""

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QLabel, QMainWindow, QWidget

from about_window import AboutWindow
from settings_window import SettingsWindow
from src.core.total_stats import TotalStats


base_dir = os.path.dirname(__file__)


class TotalStatsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(base_dir, "total_stats_widget.ui"), self)
        self.setStyleSheet(open(os.path.join(base_dir,"stylesheet.css")).read())

        self.total_stats = TotalStats()

        self.setup_stats_update()

    def setup_stats_update(self):
        self.timer = QTimer()
        self.timer.setInterval(100) # Every 0.1 seconds
        self.timer.timeout.connect(self.add_new_labels)
        self.timer.start()

    def add_new_labels(self):
        new_learnt_text = self.get_total_learnt_text()
        new_review_text = self.get_total_review_text()
        self.total_learnt_label.setText(new_learnt_text)
        self.total_review_label.setText(new_review_text)
        
    def get_total_learnt_text(self):
        learnt_msg = ("<b><font color='darkgreen'>" 
                      + str(self.total_stats.total_words_learnt())
                      + "</font></b>")
        if self.total_stats.total_words_learnt() == 1:
            learnt_msg += " word learnt."
        else:
            learnt_msg += " words learnt."
        return learnt_msg

    def get_total_review_text(self):
        review_msg = ("<b><font color='darkred'>"
                      + str(self.total_stats.total_words_to_review())
                      + "</font></b>")
        if self.total_stats.total_words_to_review() == 1:
            review_msg += " word to review."
        else:
            review_msg += " words to review."
        return review_msg



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TotalStatsWidget()
    window.show()
    app.exec_()
