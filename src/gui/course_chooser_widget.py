"""course_chooser.py"""

from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget


class CourseChooserWidget(QMainWindow):
    def __init__(self):
        super().__init__()
#        uic.loadUi(os.path.join(base_dir, "course_chooser_widget.ui"), self)
        uic.loadUi(str(Path(__file__).parents[0] / "course_chooser_widget.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CourseChooser()
    window.show()
    app.exec_()
