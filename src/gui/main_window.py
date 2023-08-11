"""main_window.py"""

import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout

from header import Header
from total_stats_widget import TotalStatsWidget
from src.core.total_stats import TotalStats
from course_chooser_widget import CourseChooserWidget

base_dir = os.path.dirname(__file__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(open(os.path.join(base_dir,"stylesheet.css")).read())
        self.setFixedSize(900, 600)

        self.setWindowTitle("Let's Learn Some Vocabulary!")

        self.layout = QVBoxLayout()

        self.header_widget = Header()
        self.layout.addWidget(self.header_widget)

        self.total_stats_widget = TotalStatsWidget()
        self.layout.addWidget(self.total_stats_widget)
        self.layout.setSpacing(10)

        self.course_chooser = CourseChooserWidget()
        self.layout.addWidget(self.course_chooser)

        self.layout.setSpacing(10)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
