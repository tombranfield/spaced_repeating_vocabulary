"""browse_course_window.py"""


from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QTabWidget, QGridLayout

from src.core.course import Course
from src.database.courses_dao import CoursesDAO


class BrowseCourseWindow(QDialog):
    """A window for the user to delete the course"""
    def __init__(self, course, parent=None):
        super(BrowseCourseWindow, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "browse_course_window.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())
        self.course_name = course.name
        self.setup_widgets()
        self._NUM_WORDS_PER_TAB = 100

    def setup_widgets(self):
        """Connects widget signals and slots"""
        self.close_button.clicked.connect(self.close_window)
        self.setup_course_names_box()
        self.course_names_box.currentTextChanged.connect(
            self.existing_course_name_changed)
        self.tab_widget = self.get_tab_widget()

    def setup_course_names_box(self):
        courses_dao = CoursesDAO()
        course_names = courses_dao.courses_list()
        self.course_names_box.addItems(course_names)
        course_index = course_names.index(self.course_name)
        self.course_names_box.setCurrentIndex(course_index)

    def existing_course_name_changed(self):
        pass

    def close_window(self):
        """Closes the window"""
        self.close()

   def get_tab_widget(self):
        # Need num of words in list
        # TODO
        num_words = 1000
        num_words_per_tab = 25
        num_tabs = math.ceil(num_words / self._NUM_WORDS_PER_TAB)
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.North)
        # TODO write create_tab
        first_tab = self.create_tab(0)
        tab_widget.addTab(first_tab, "1")
        for tab_num in range(2, num_tabs + 1):
            tab = QWidget()
            tab_widget.addTab(tab, str(tab_num))
            tab.layout = QGridLayout()
            tab.setLayout(tab.layout)
        return tab_widget

    def create_tab(self, tab_index):
        tab = QWidget()
        tab.layout = QGridLayout()

        starting_offset = tab_index * self._NUM_WORDS_PER_TAB
        if starting_offset + 100 > self.num_words:
            max = self.num_words
        else:
            max = starting_offset + self._NUM_WORDS_PER_TAB

