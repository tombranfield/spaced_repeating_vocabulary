"""header.py"""


from pathlib import Path
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QWidget

from about_window import AboutWindow
from settings_window import SettingsWindow


class Header(QWidget):
    def __init__(self):
        """Header class which holds the about and settings buttons"""
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "header.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.about_button.clicked.connect(self.open_about_window)
        self.settings_button.clicked.connect(self.open_settings_window)
        self.exit_button.clicked.connect(self.close_window)

    def open_about_window(self):
        dialog = AboutWindow(self)
        dialog.exec_()

    def open_settings_window(self):
        dialog = SettingsWindow(self)
        dialog.exec_()

    def close_window(self):
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Header()
    window.show()
    app.exec_()
