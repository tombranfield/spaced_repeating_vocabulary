"""course_chooser.py"""


from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QMainWindow, QWidget

from src.core.total_stats import TotalStats
from src.database.courses_dao import CoursesDAO
from insert_from_file_window import InsertFromFileWindow
from new_course_window import NewCourseWindow
from delete_course_window import DeleteCourseWindow


class CourseChooserWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(Path(__file__).parents[0] / "course_chooser_widget.ui"), self)
        self.setStyleSheet(open(str(Path("stylesheet.css"))).read())
        self.course_name = self.course_names_box.currentText()
        self.total_stats = TotalStats()
        self.setup_widgets()

    def setup_widgets(self):
        self.course_names_box.currentTextChanged.connect(
            self.existing_course_name_changed)
        self.new_course_button.clicked.connect(self.open_new_course_window)
        self.delete_course_button.clicked.connect(self.delete_course_window)
        self.insert_from_file_button.clicked.connect(self.insert_from_file_window)
        self.setup_course_names_box()
        self.refresh_widgets()
        self.refresh_labels()

    def refresh_widgets(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.refresh_menu_buttons)
        self.timer.timeout.connect(self.refresh_learn_button)
        self.timer.timeout.connect(self.refresh_review_button)
        self.refresh_labels()
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

    def insert_from_file_window(self):
        dialog = InsertFromFileWindow(self.course_name, parent=self)
        dialog.exec_()

    def existing_course_name_changed(self, course_name):
        self.course_name = course_name
        self.refresh_labels()
        self.refresh_learn_button()
        self.refresh_review_button()

    def refresh_labels(self):
        new_learnt_text = self.get_total_learnt_text()
        new_review_text = self.get_total_review_text()
        self.known_words_label.setText(new_learnt_text)
        self.review_words_label.setText(new_review_text)

    def refresh_learn_button(self):
        if self.total_stats.total_words_to_learn(self.course_name) == 0:
            self.learn_button.setEnabled(False)
            self.learn_button.setStyleSheet("background: lightgray")
        else:
            self.learn_button.setEnabled(True)
            self.learn_button.setStyleSheet("background: lime")

    def refresh_review_button(self):
        if self.total_stats.total_words_to_review(self.course_name) == 0:
            self.review_button.setEnabled(False)
            self.review_button.setStyleSheet("background: lightgray")
        else:
            self.review_button.setEnabled(True)
            self.review_button.setStyleSheet("background: lime")

    def get_total_learnt_text(self):
        total_words = self.total_stats.total_words(self.course_name)
        num_words_learnt = self.total_stats.total_words_learnt(self.course_name)
        learnt_msg = ("<b><font color='green'>"
                      + str(num_words_learnt)
                      + "/" + str(total_words)
                      + "</font></b>")
        if num_words_learnt == 1:
            learnt_msg += " word learnt"
        else:
            learnt_msg += " words learnt"
        return learnt_msg

    def get_total_review_text(self):
        num_review_words = self.total_stats.total_words_to_review(self.course_name)
        review_msg = "<b><font color=\'"
        if num_review_words == 0:
            review_msg += "green\'>"
        else:
            review_msg += "darkred\'>"
        review_msg += (str(num_review_words)) + "</font></b>"
        if num_review_words == 1:
            review_msg += " word to review"
        else:
            review_msg += " words to review"
        return review_msg

    def refresh_menu_buttons(self):
        if self.course_name == "":
            self.delete_course_button.setEnabled(False)
            self.browse_words_button.setEnabled(False)
            self.insert_from_file_button.setEnabled(False)
            self.delete_course_button.setStyleSheet("color: gray")
            self.browse_words_button.setStyleSheet("color: gray")
            self.insert_from_file_button.setStyleSheet("color: gray")
        else:
            self.delete_course_button.setEnabled(True)
            self.browse_words_button.setEnabled(True)
            self.insert_from_file_button.setEnabled(True)
            self.delete_course_button.setStyleSheet("color: black")
            self.browse_words_button.setStyleSheet("color: black")
            self.insert_from_file_button.setStyleSheet("color: black")
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CourseChooser()
    window.show()
    app.exec_()
