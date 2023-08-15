"""quiz.py"""


from pathlib import Path
import random
import time
from typing import Literal

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
)

from src.core.quiz_word_selector import QuizWordSelector
from src.core.settings import Settings
from src.gui.quiz_definition import QuizDefinition
from src.gui.quiz_multiple_choice import QuizMultipleChoice
from src.gui.quiz_preview import QuizPreview
from src.gui.quiz_typing_test import QuizTypingTest


_QUIZ_TYPE = Literal["learn", "review"]


class Quiz(QDialog):
    """Quiz for learning or reviewing words"""
    def __init__(self, course_name, learn_or_review: _QUIZ_TYPE, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.course_name = course_name
        self.quiz_type = learn_or_review

        # Import settings
        self.settings = Settings()        
        self.max_learn_words = self.settings.max_learn_words

        # Setup the quiz words
        self.quiz_word_selector = QuizWordSelector(self.course_name)
        self.words_to_learn = self.quiz_word_selector.words_to_learn()
        self.all_course_words = self.quiz_word_selector.all_course_words()
        self.num_words_to_quiz = self.get_num_words_to_quiz()
        self.words_to_quiz = list(self.words_to_learn[:self.num_words_to_quiz])

        # Setup the progress bar
        # TODO why 7 - why did I choose this?
        self.max_progress = 7 * len(self.words_to_quiz)
        self.progress_bar.setRange(0, self.max_progress)

        # Initialize the active quiz word
        self.active_quiz_word = self.words_to_quiz[0]
        self.active_quiz_words = []

        # Initialize the quiz widgets
        self.setup_quit_button()
        self.preview_widget = QuizPreview(
            self.words_to_quiz,
            "learn",    
            parent=self
        )
        self.definition_widget = QuizDefinition(
            self.active_quiz_word,
            parent=self
        )
        self.multiple_choice = QuizMultipleChoice(
            self.active_quiz_word,
            self.all_course_words,
            "english_to_foreign",
            parent=self
        )
        self.typing_test = QuizTypingTest(
            self.active_quiz_word,
            parent=self
        )

        # TODO debugging combobox
        self.choose_page_box.currentIndexChanged[str].connect(
            self.choose_page_changed
        )
        self.choose_page_box.clearFocus()
        self.choose_page_box.setEnabled(True)

        # Add the quiz widgets to the layout
        self.stacked_layout.insertWidget(0, self.preview_widget)    
        self.stacked_layout.insertWidget(1, self.multiple_choice)
        self.stacked_layout.insertWidget(2, self.definition_widget)
        self.stacked_layout.insertWidget(3, self.typing_test)
        self.stacked_layout.setCurrentIndex(0)

        self.previous_quiz = None
        self.is_quiz_correct = None    


    def start_slot(self, a):
        print("START SLOT CALLED")
        self.play_next()

    def next_slot(self, a):
        print("NEXT SLOT CALLED")
        self.is_quiz_correct = 1
        self.play_next()

    def is_correct_slot(self, a):
        print("IS CORRECT SLOT CALLED")
        self.is_quiz_correct = a
        self.play_next()

    def play_next(self):
        if self.previous_quiz:
            self.apply_quiz_results()
            self.is_quiz_correct = None
            self.set_progress()
            self.show_answers_pause(self.previous_quiz)
        if self.is_add_new_active_word():
            self.add_new_active_words(self.num_active_words_to_add())
        if self.is_quiz_finished():
            self.finish_quiz()
            return
        while True:
            next_active_word = self.get_random_active_word()
            self.active_quiz_word = next_active_word
            next_quiz = next_active_word.get_next_quiz()
            break
        self.do_next_quiz(next_active_word, next_quiz)
        self.previous_quiz = next_quiz

    def apply_quiz_results(self):
        if self.previous_quiz in ["word_definition", "word_defintion_typing"]:
            self.active_quiz_word.set_next()
        elif self.previous_quiz in [
            "english_to_foreign_multiple_quiz",
            "foreign_to_english_multiple_quiz",
        ]:
            if self.is_quiz_correct:
                self.active_quiz_word.set_correct()
            else:
                self.active_quiz_word.set_incorrect_multiple_quiz()
        elif self.previous_quiz == "typing_quiz":
            if self.is_quiz_correct:
                self.active_quiz_word.set_correct()
            else:
                self.active_quiz_word.set_incorrect_typing_quiz()

    def show_answers_pause(self, previous_quiz):
        if previous_quiz not in ["word_definition", "word_definition_typing"]:
            time.sleep(1)

    def get_num_words_to_quiz(self):
        return min(len(self.words_to_learn), self.max_learn_words)

    def setup_quit_button(self):
        self.quit_button.setDefault(False)
        self.quit_button.setAutoDefault(False)
        self.quit_button.clicked.connect(self.quit_quiz)       

    def quit_quiz(self):
        quit_dialog = QMessageBox(self)
        quit_dialog.setIcon(QMessageBox.Warning)
        quit_dialog.setWindowTitle("Quitting")
        msg = "Do you want to leave the quiz? All progress will be lost."
        quit_dialog.setText(msg)
        quit_dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        button = quit_dialog.exec_()
        if button == QMessageBox.Cancel:
            return
        self.close()



    # TODO remove this
    def choose_page_changed(self, s):
        new_page_index = int(s)
        self.stacked_layout.setCurrentIndex(new_page_index)
