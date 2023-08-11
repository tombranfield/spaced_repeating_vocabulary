"""quiz.py"""


from pathlib import Path
from typing import Literal

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from src.core.quiz_word_selector import QuizWordSelector
from src.core.settings import Settings
from src.gui.quiz_preview import QuizPreview


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
        self.max_progress = 7 * len(self.words_to_quiz)
        self.progress_bar.setRange(0, self.max_progress)

        # Initialize the active quiz word


        # Initialize the quiz widgets
        self.quit_button.clicked.connect(self.close_window)       
        self.preview_widget = QuizPreview(
            self.words_to_quiz,
            "learn",    
            parent=self
        )

        # TODO debugging combobox
        self.choose_page_box.currentIndexChanged[str].connect(
            self.choose_page_changed
        )

        # Add the quiz widgets to the layout
        self.stacked_layout.insertWidget(0, self.preview_widget)    



        self.stacked_layout.setCurrentIndex(0)

    def initialize_quiz_widgets(self):
        # More widgets underneath
        pass


    def add_quiz_widgets_to_stacked_layout(self):
        pass

    def get_num_words_to_quiz(self):
        return min(len(self.words_to_learn), self.max_learn_words)

    def close_window(self):
        self.close()

    def start_slot(self, a):
        self.play_next()

    def play_next(self):
        pass


    # TODO remove this
    def choose_page_changed(self, s):
        new_page_index = int(s)
        self.stacked_layout.setCurrentIndex(new_page_index)
