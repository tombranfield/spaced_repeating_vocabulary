"""course_chooser.py"""


from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget

from src.database.courses_dao import CoursesDAO


class CourseChooserWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "course_chooser_widget.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())
        self.setup_widgets()

    def setup_widgets(self):
        self.setup_course_names_box()
        self.course_names_box.highlighted.connect(self.setup_course_names_box)
        self.refresh_widgets()

    def refresh_widgets(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        # self.timer.timeout.connect(self.setup_course_names_box)
        # self.timer.timeout.connect(self.update_learn_button)
        # self.timer.timeout.connect(self.update_review_button)
        self.timer.start()

    def setup_course_names_box(self):
        courses_dao = CoursesDAO()
        course_names = courses_dao.courses_list()
        self.course_names_box.clear()
        self.course_names_box.addItems(course_names)        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CourseChooser()
    window.show()
    app.exec_()
