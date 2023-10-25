"""browse_course_window.py"""


import math
from pathlib import Path
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QDialog, 
    QTabWidget, 
    QGridLayout, 
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QIcon


from src.core.course import Course
from src.core.row import Row
from src.database.courses_dao import CoursesDAO
from src.database.row_dao import RowDAO



class BrowseCourseWindow(QDialog):
    """A window for the user to browse the course words"""
    def __init__(self, course, parent=None):
        super(BrowseCourseWindow, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "browse_course_window.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())
        self.course_name = course.name
        self.course_words = self.get_course_words()
        self.new_foreign_word = ""
        self.new_trans_word = ""
        self.setup_widgets()
        self._NUM_WORDS_PER_TAB = 100
        self.tab_widget = self.get_tab_widget()
        self.tab_widget.currentChanged.connect(self.tabs_changed)
        self.scroll_area.setWidget(self.tab_widget)

    def setup_widgets(self):
        """Connects widget signals and slots"""
        self.close_button.clicked.connect(self.close_window)
        self.insert_word_button.clicked.connect(self.insert_new_word)
        self.foreign_word_lineEdit.textChanged.connect(
            self.new_foreign_word_text_changed)
        self.trans_word_lineEdit.textChanged.connect(
            self.new_trans_word_text_changed)
        self.set_insert_new_word_button_status()        

    def close_window(self):
        """Closes the window"""
        self.close()

    def new_foreign_word_text_changed(self, new_text):
        self.new_foreign_word = new_text
        self.set_insert_new_word_button_status()

    def new_trans_word_text_changed(self, new_text):
        self.new_trans_word = new_text
        self.set_insert_new_word_button_status()

    def insert_new_word(self):
        courses_dao = CoursesDAO()
        language = courses_dao.language(self.course_name)
        new_row = Row(self.new_foreign_word, self.new_trans_word,
                      language, self.course_name)
        row_dao = RowDAO()
        row_dao.insert_row(new_row)
        self.foreign_word_lineEdit.setText("")
        self.trans_word_lineEdit.setText("")
        self.refresh_tab_widget()
        self.move_to_last_tab()
        self.scroll_to_bottom()

    def refresh_tab_widget(self):
        self.course_words = self.get_course_words()
        self.tab_widget = self.get_tab_widget()
        self.tab_widget.currentChanged.connect(self.tabs_changed)
        self.scroll_area.setWidget(self.tab_widget)

    def set_insert_new_word_button_status(self):
        if self.new_foreign_word and self.new_trans_word:
            self.insert_word_button.setStyleSheet("background: lime")
            self.insert_word_button.setEnabled(True)
        else:
            self.insert_word_button.setStyleSheet("background: gray")
            self.insert_word_button.setEnabled(False)

    def get_course_words(self):
        courses_dao = CoursesDAO()
        course_words = courses_dao.course_words(self.course_name)
        return course_words

    def get_review_time_remaining(self, when_review):
        now = datetime.now()
        when_review = when_review.rstrip()
        when_review = datetime.strptime(when_review,
            "%d/%m/%Y %H:%M:%S")
        if now > when_review:
            return "Review <b>now</b>"
        else:
            diff = when_review - now
            if abs(diff.days) >= 1:
                return "Review in " + str(abs(diff.days)) + " days"
            num_hours = math.ceil(diff.seconds / 3600)
            if num_hours > 1:
                return "Review in " + str(num_hours) + " hours"
            else:
                num_minutes = math.ceil(diff.seconds / 60)
                return "Review in " + str(num_minutes) + " minutes"

    def get_num_tabs(self):
        num_words = len(self.course_words)
        num_words_per_tab = 25
        num_tabs = math.ceil(num_words / self._NUM_WORDS_PER_TAB)
        return num_tabs

    def move_to_last_tab(self):
        num_tabs = self.get_num_tabs()
        final_tab_index = num_tabs - 1
        self.tab_widget.setCurrentIndex(final_tab_index)

    def scroll_to_bottom(self):
        fract_pos_down = self.get_fract_pos_down_of_final_tab()
        max = self.scroll_area.verticalScrollBar().maximum()
        down_pos = math.floor(fract_pos_down * max)
        self.scroll_area.verticalScrollBar().setValue(down_pos)

        """
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )
        """

    def get_fract_pos_down_of_final_tab(self):
        final_tab_index = self.get_num_tabs() - 1
        starting_offset = final_tab_index * self._NUM_WORDS_PER_TAB
        max = self.get_max_offset(starting_offset)
        fract_down = (max - starting_offset) / self._NUM_WORDS_PER_TAB
        return fract_down


    def get_tab_widget(self):
        """
        num_words = len(self.course_words)
        num_words_per_tab = 25
        num_tabs = math.ceil(num_words / self._NUM_WORDS_PER_TAB)
        """
        num_tabs = self.get_num_tabs()
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.North)
        first_tab = self.create_tab(0)
        tab_widget.addTab(first_tab, "1")
        for tab_num in range(2, num_tabs + 1):
            tab = QWidget()
            tab_widget.addTab(tab, str(tab_num))
            #TODO I don't know what below does
            #tab.layout = QGridLayout()
            #tab.setLayout(tab.layout)
        return tab_widget

    def get_max_offset(self, starting_offset):
        if starting_offset + 100 > len(self.course_words):
            max = len(self.course_words)
        else:
            max = starting_offset + self._NUM_WORDS_PER_TAB
        return max        
        
    def get_delete_button(self, row_id):
        delete_button = QPushButton()
        img_path = str(Path(__file__).parents[2] / "data/cross.png")
        delete_pixmap = QPixmap(img_path)
        delete_button.setIcon(QIcon(delete_pixmap))
        delete_button.setDefault(False)
        delete_button.setAutoDefault(False)
        delete_button.clicked.connect(
            lambda clicked, id=row_id : self.delete_row(clicked, id)
        )
        return delete_button

    def delete_row(self, clicked, id):
        #TODO refactor, separate function for msg box and tab moving
        dlg = QMessageBox(self)
        dlg.setIcon(QMessageBox.Warning)
        dlg.setWindowTitle("Confirm deletion")
        msg = "Do you really want to delete this?"
        dlg.setText(msg)
        dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        button = dlg.exec_()
        if button == QMessageBox.Cancel:
            return
        courses_dao = CoursesDAO()
        courses_dao.delete_word(id)
        current_tab_index = self.tab_widget.currentIndex()
        self.refresh_tab_widget()
        try:
            self.tab_widget.setCurrentIndex(current_tab_index)
        except:
            self.tab_widget.setCurrentIndex(current_tab_index-1)


    def get_foreign_word_entry(self, row_id, foreign_word):
        foreign_word_entry = QLineEdit(foreign_word)
        foreign_word_entry.textEdited.connect(
            lambda x, id=row_id : self.foreign_word_edited(id, x)
        )
        return foreign_word_entry

    def foreign_word_edited(self, row_id, new_text):
        courses_dao = CoursesDAO()
        courses_dao.change_foreign_word(row_id, new_text)

    def get_trans_word_entry(self, row_id, translated_word):
        translated_word_entry = QLineEdit(translated_word)
        translated_word_entry.textEdited.connect(
            lambda x, id=row_id : self.translated_word_edited(id, x)
        )
        return translated_word_entry

    def translated_word_edited(self, row_id, new_text):
        courses_dao = CoursesDAO()
        courses_dao.change_translated_word(row_id, new_text)

    def get_is_known_label(self, is_known):
        if is_known:
            msg = "<font color='green'>" + "KNOWN" + "</font>"
        else:
            msg = "<font color='red'>" + "UNKNOWN" + "</font>"
        return QLabel(msg)


    def create_tab(self, tab_index):
        tab = QWidget()
        tab.layout = QGridLayout()

        starting_offset = tab_index * self._NUM_WORDS_PER_TAB
        max = self.get_max_offset(starting_offset)

        for i in range(starting_offset, max):
            row = self.course_words[i]

            # Get widgets to put on each row of the tab
            delete_button = self.get_delete_button(row.id)
            foreign_word_entry = self.get_foreign_word_entry(
                row.id, row.foreign_word
            )
            translated_word_entry = self.get_trans_word_entry(
                row.id, row.translated_word
            )
            is_known_label = self.get_is_known_label(row.is_known)
            when_review_label = QLabel(row.when_review)

            # Add widgets to the tab's grid layout
            tab.layout.addWidget(delete_button, i, 0)
            tab.layout.addWidget(foreign_word_entry, i, 2)
            tab.layout.addWidget(translated_word_entry, i, 3)
            tab.layout.addWidget(is_known_label, i, 4)
            tab.layout.addWidget(when_review_label, i, 5, 1, 2)

        # Adding empty labels to the grid layout to add as empty space
        empty_label = QLabel("")
        if (max - starting_offset) < self._NUM_WORDS_PER_TAB:
            for i in range(max, max + self._NUM_WORDS_PER_TAB):
                tab.layout.addWidget(QLabel(""), i, 0)

        tab.setLayout(tab.layout)
        return tab


    def tabs_changed(self, tab_index):
        self.tab_widget.currentChanged.disconnect()
        tab_name = str(tab_index + 1)

        # Create a new tab widget
        tab = self.create_tab(tab_index)
        
        # Remove the previous tab and insert a new one
        current_index = tab_index
        self.tab_widget.removeTab(current_index)
        self.tab_widget.insertTab(current_index, tab, tab_name)
        self.tab_widget.setCurrentIndex(current_index)

        self.tab_widget.currentChanged.connect(self.tabs_changed)
