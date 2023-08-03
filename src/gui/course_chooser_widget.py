"""course_chooser.py"""


from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget

from src.database.courses_dao import CoursesDAO
from new_course_window import NewCourseWindow
from delete_course_window import DeleteCourseWindow


class CourseChooserWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "course_chooser_widget.ui"), self)
        self.setStyleSheet(open("stylesheet.css").read())
        self.setup_widgets()
        self.course_name = self.course_names_box.currentText()

    def setup_widgets(self):
        self.course_names_box.currentTextChanged.connect(
            self.existing_course_name_changed)
        self.new_course_button.clicked.connect(self.open_new_course_window)
        self.delete_course_button.clicked.connect(self.delete_course_window)
        self.setup_course_names_box()
        self.refresh_widgets()

    def refresh_widgets(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_delete_course_button)
        # self.timer.timeout.connect(self.update_learn_button)
        # self.timer.timeout.connect(self.update_review_button)
        self.timer.start()

    def setup_course_names_box(self):
        courses_dao = CoursesDAO()
        course_names = courses_dao.courses_list()
        self.course_names_box.clear()
        self.course_names_box.addItems(course_names)        

    def open_new_course_window(self):
        dialog = NewCourseWindow(self)
        dialog.exec_()
        self.setup_course_names_box()

    def delete_course_window(self):
        dialog = DeleteCourseWindow(self.course_name, parent=self)
        dialog.exec_()
        self.setup_course_names_box()

    def existing_course_name_changed(self, course_name):
        self.course_name = course_name
        # get new stats
        # set the new labels
    
    def update_delete_course_button(self):
        if self.course_name == "":
            self.delete_course_button.setEnabled(False)
            self.delete_course_button.setStyleSheet("color: gray")
        else:
            self.delete_course_button.setEnabled(True)
            self.delete_course_button.setStyleSheet("color: black")
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CourseChooser()
    window.show()
    app.exec_()
