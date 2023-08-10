"""quiz.py"""


from pathlib import Path
from typing import Literal

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from src.core.quiz_word_selector import QuizWordSelector
from src.core.settings import Settings

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
        self.words_to_quiz = list(self.words_to_learn[:5])
    
        # Setup the progress bar


        self.quit_button.clicked.connect(self.close_window)       
    

    def initialize_quiz_widgets(self):
        self.preview_widget = QuizPreview(
            self.words_to_quiz,
            "learn",    
            parent=self)
        # More underneath
        # Need list_words, and words_to_quiz

    def add_quiz_widgets_to_stacked_layout(self):
        pass

    def setup_progress_bar(self):
        pass

    def close_window(self):
        self.close()
