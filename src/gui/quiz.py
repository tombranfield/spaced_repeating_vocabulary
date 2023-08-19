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
from src.database.quiz_word_dao import QuizWordDAO
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
        self.max_review_words = self.settings.max_review_words

        # Setup the quiz words
        self.quiz_word_selector = QuizWordSelector(self.course_name)
        self.words_to_learn = self.quiz_word_selector.words_to_learn()
        self.words_to_review = self.quiz_word_selector.words_to_review()
        self.all_course_words = self.quiz_word_selector.all_course_words()
        self.num_words_to_quiz = self.get_num_words_to_quiz()
#        self.words_to_quiz = list(self.words_to_learn[:self.num_words_to_quiz])
        self.words_to_quiz = self.get_words_to_quiz(self.num_words_to_quiz)

        # TODO checking we are loading the correct words
        print("Quiz type:", self.quiz_type)
        for quiz_word in self.words_to_quiz:
            print(quiz_word.foreign_word)

        # Initialize the active quiz word
        self.active_quiz_word = self.words_to_quiz[0]
        self.active_quiz_word.quiz_type = self.quiz_type
        self.active_quiz_words = []

        # Setup the progress bar
        self.max_progress = (
            self.active_quiz_word.max_progress_score * len(self.words_to_quiz)
        )
        self.progress_bar.setRange(0, self.max_progress)
        self.progress_bar.setValue(0)

        # Initialize the quiz widgets
        self.setup_quit_button()
        self.preview_widget = QuizPreview(
            self.words_to_quiz,
            self.quiz_type,    
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

        # Add the quiz widgets to the layout
        self.stacked_layout.insertWidget(0, self.preview_widget)    
        self.stacked_layout.insertWidget(1, self.multiple_choice)
        self.stacked_layout.insertWidget(2, self.definition_widget)
        self.stacked_layout.insertWidget(3, self.typing_test)
        self.stacked_layout.setCurrentIndex(0)

        self.previous_quiz = None
        self.is_quiz_correct = None    

    def start_slot(self, a):
        self.play_next()

    def next_slot(self, a):
        self.is_quiz_correct = 1
        self.play_next()

    def is_correct_slot(self, a):
        self.is_quiz_correct = a
        self.play_next()

    def play_next(self):
        if self.previous_quiz:
            self.apply_quiz_results()
            self.is_quiz_correct = None
            self.set_progress()
        if self.is_add_new_active_quiz_word():
            self.add_new_active_quiz_words(self.num_active_quiz_words_to_add())
        if self.is_quiz_finished():
            self.finish_quiz()
            return
        while True:
            self.active_quiz_word = random.choice(self.active_quiz_words)
            if not self.active_quiz_word.is_quizzing_finished():
                next_quiz = self.active_quiz_word.get_next_quiz()
                break
        self.do_next_quiz(self.active_quiz_word, next_quiz)
        self.previous_quiz = next_quiz

    def apply_quiz_results(self):
        if self.previous_quiz in ["word_definition", "word_definition_typing"]:
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

    def is_add_new_active_quiz_word(self):
        if not self.words_to_quiz:
            return False
        for quiz_word in self.active_quiz_words:
            if quiz_word.progress_score < 3:
                return False
        return True

    def add_new_active_quiz_words(self, num_to_add):
        for n in range(num_to_add):
            self.add_new_active_quiz_word()

    def add_new_active_quiz_word(self):
        rand_index = random.randint(0, len(self.words_to_quiz) - 1)
        rand_quiz_word = self.words_to_quiz.pop(rand_index)
        rand_quiz_word.quiz_type = self.quiz_type
        self.active_quiz_words.append(rand_quiz_word)

    def num_active_quiz_words_to_add(self):
        if len(self.words_to_quiz) - len(self.active_quiz_words) == 1:
            return 1
        return 2        

    def get_num_words_to_quiz(self):
        if self.quiz_type == "learn":
            return min(len(self.words_to_learn), self.max_learn_words)
        elif self.quiz_type == "review":
            return min(len(self.words_to_review), self.max_review_words)

    def get_words_to_quiz(self, num_words_to_quiz):
        if self.quiz_type == "learn":
            return list(self.words_to_learn[:num_words_to_quiz])
        elif self.quiz_type == "review":
            return list(self.words_to_review[:num_words_to_quiz])

    def is_quiz_finished(self):
        if self.words_to_quiz:
            return False
        for quiz_word in self.active_quiz_words:
            if not quiz_word.is_quizzing_finished():
                return False
        return True

    def finish_quiz(self):
        self.apply_results_to_database()
        messagebox = self.finish_messagebox()
        button = messagebox.exec_()
        if button == QMessageBox.Ok:
            self.close()        

    def apply_results_to_database(self):
        if self.quiz_type == "learn":
            for quiz_word in self.active_quiz_words:
                quiz_word_dao = QuizWordDAO(quiz_word)
                quiz_word_dao.add_num_correct(quiz_word.num_correct)
                quiz_word_dao.add_num_incorrect(quiz_word.num_incorrect)
                quiz_word_dao.set_as_learnt()
        elif self.quiz_type == "review":
            print("reviewing to db not implemented yet :)")
            for quiz_word in self.active_quiz_words:
                pass
                """
                quiz_word_dao = QuizWordDAO(quiz_word)
                quiz_word_dao.add_num_correct(quiz_word.num_correct)
                quiz_word_dao.add_num_incorrect(quiz_word.num_incorrect)
                quiz_word_dao.finished_reviewing(quiz_word.was_review_correct)
                """

    def finish_messagebox(self):
        messagebox = QMessageBox(self)
        messagebox.setIcon(QMessageBox.Information)
        messagebox.setWindowTitle("Quiz Complete")
        msg = self.get_finish_msg()
        messagebox.setText(msg)
        messagebox.setStandardButtons(QMessageBox.Ok)
        return messagebox

    def get_finish_msg(self):
        msg = "         Congratulations!                   \n"
        if self.quiz_type == "learn":
            msg += "         You have learned:\n\n"
            for quiz_word in self.active_quiz_words:
                msg += "          -" + quiz_word.foreign_word + "\n"
        elif self.quiz_type == "review":
            msg += "         You have reviewed " + str(self.num_words_to_quiz)
            if self.num_words_to_quiz == 1:
                msg += " word!"
            else:
                msg += " words!"
        return msg

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

    def do_next_quiz(self, active_quiz_word, next_quiz):
        if next_quiz == "word_definition":
            self.do_word_definition_quiz(self.active_quiz_word, is_typing=False)
        elif next_quiz == "word_definition_typing":
            self.do_word_definition_quiz(self.active_quiz_word, is_typing=True)
        elif next_quiz == "foreign_to_english_multiple_quiz":
            self.do_foreign_to_english_multiple_quiz(self.active_quiz_word)
        elif next_quiz == "english_to_foreign_multiple_quiz":
            self.do_english_to_foreign_multiple_quiz(self.active_quiz_word)
        elif next_quiz == "typing_quiz":
            self.do_typing_quiz(self.active_quiz_word)

    def do_word_definition_quiz(self, active_quiz_word, is_typing):
        self.definition_widget = QuizDefinition(
            self.active_quiz_word,
            is_typing,  
            parent=self,
        )
        self.stacked_layout.insertWidget(2, self.definition_widget)
        self.stacked_layout.setCurrentIndex(2)

    def do_foreign_to_english_multiple_quiz(self, active_quiz_word):
        self.do_multiple_quiz(active_quiz_word, "foreign_to_english")

    def do_english_to_foreign_multiple_quiz(self, active_quiz_word):
        self.do_multiple_quiz(active_quiz_word, "english_to_foreign")

    def do_multiple_quiz(self, active_quiz_word, mode):
        self.multiple_choice = QuizMultipleChoice(
            self.active_quiz_word,
            self.all_course_words,
            mode,   
            parent=self,
        )
        self.stacked_layout.insertWidget(1, self.multiple_choice)
        self.stacked_layout.setCurrentIndex(1)
    
    def do_typing_quiz(self, active_quiz_word):
        self.typing_test = QuizTypingTest(
            self.active_quiz_word,
            parent=self
        )
        self.stacked_layout.insertWidget(3, self.typing_test)
        self.stacked_layout.setCurrentIndex(3)

    def set_progress(self):
        progress = self.get_progress()
        max_progress = self.get_max_progress()
        self.progress_bar.setMaximum(max_progress)
        self.progress_bar.setValue(0)
        self.progress_bar.setValue(progress)

    def get_progress(self):
        progress = 0
        for quiz_word in self.active_quiz_words:
            progress += quiz_word.progress_score
        return progress

    def get_max_progress(self):
        max_progress = 0
        for quiz_word in self.active_quiz_words:
            max_progress += quiz_word.max_progress_score
        for quiz_word in self.words_to_quiz:
            max_progress += quiz_word.max_progress_score
        return max_progress
