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
        self.row_entries = self.get_row_entries()
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

    def get_row_entries(self):
        #TODO
        words = self.get_words_of_list(list_name)
        row_entries = [list(t) for t in words]
        for l in row_entries:
            # Magic Numbers. Convert words to classes, not arrays
            # ie database function get_words_of_list should return
            # a row class, then get/set elements using methods
            if l[3] == 0:
                l[4] = "        "
            else:
                when_review = l[4]
                review_string = self.get_review_time_remaining(when_review)
                l[4] = review_string
        return row_entries



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

        for i in range(starting_offset, max):
            row_id = self.row_entries[i][0]
            foreign_word = self.row_entries[i][1]
            translated_word = self.row_entries[i][2]
            is_known = self.row_entries[i][3]
            when_review = self.row_entries[i][4]

            delete_button = self.get_delete_button()
            delete_button.setDefault(False)
            delete_button.setAutoDefault(False)
            delete_button.clicked.connect(
                         lambda clicked, id=row_id : self.delete_row(clicked, id))

            empty_lab = QLabel("")

            foreign_word_entry = QLineEdit(foreign_word)
            foreign_word_entry.textEdited.connect(
                           lambda x, id=row_id : self.foreign_word_edited(x, id))

            translated_word_entry = QLineEdit(translated_word)
            translated_word_entry.textEdited.connect(
                       lambda x, id=row_id : self.translated_word_edited(x, id))

            is_known_label = self.get_is_known_label(is_known)

            when_review_label = QLabel(when_review)

            tab.layout.addWidget(delete_button, i, 0)
            tab.layout.addWidget(empty_lab, i, 1)
            tab.layout.addWidget(foreign_word_entry, i, 2)
            tab.layout.addWidget(translated_word_entry, i, 3)
            tab.layout.addWidget(is_known_label, i, 4)
            tab.layout.addWidget(when_review_label, i, 5, 1, 2)

        tab.setLayout(tab.layout)
        return tab

