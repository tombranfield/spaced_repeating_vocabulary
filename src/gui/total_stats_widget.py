"""total_stats_widget.py"""

from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QLabel, QMainWindow, QWidget

from about_window import AboutWindow
from settings_window import SettingsWindow
from src.core.total_stats import TotalStats


class TotalStatsWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "total_stats_widget.ui"), self)
#        self.setStyleSheet(open(str(Path("stylesheet.css"))).read())
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.total_stats = TotalStats()
        self.refresh_widgets()

    def refresh_widgets(self):
        self.timer = QTimer()
        self.timer.setInterval(100) # Every 0.1 seconds
        self.timer.timeout.connect(self.add_new_labels)
        self.timer.timeout.connect(self.update_review_button)
        self.timer.start()

    def add_new_labels(self):
        new_learnt_text = self.get_total_learnt_text()
        new_review_text = self.get_total_review_text()
        self.total_learnt_label.setText(new_learnt_text)
        self.total_review_label.setText(new_review_text)
        
    def get_total_learnt_text(self):
        learnt_msg = ("<b><font color='green'>" 
                      + str(self.total_stats.total_words_learnt())
                      + "/" + str(self.total_stats.total_words())
                      + "</font></b>")
        if self.total_stats.total_words_learnt() == 1:
            learnt_msg += " word learnt"
        else:
            learnt_msg += " words learnt"
        return learnt_msg

    def get_total_review_text(self):
        total_review_words = self.total_stats.total_words_to_review()
        review_msg = "<b><font color=\'"
        if total_review_words == 0:
            review_msg += "green\'>"
        else: 
            review_msg += "darkred\'>"
        review_msg += (str(total_review_words)) + "</font></b>"
        if total_review_words == 1:
            review_msg += " word to review"
        else:
            review_msg += " words to review"
        return review_msg

    def update_review_button(self):
        if self.total_stats.total_words_to_review() == 0:
            self.review_button.setEnabled(False)
            self.review_button.setStyleSheet("background: lightgray")
        else:
            self.review_button.setEnabled(True)
            self.review_button.setStyleSheet("background: lime")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TotalStatsWidget()
    window.show()
    app.exec_()
