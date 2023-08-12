"""quiz_multiple_choice.py"""


from pathlib import Path
import random

from PyQt5 import uic
from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
)
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
)

from src.core.settings import Settings


class QuizMultipleChoice(QWidget):
    """A widget for a typing test in the quiz"""
    is_correct = pyqtSignal(int)
        
    def __init__(self, quiz_word, course_words, mode, parent=None):
        super(QuizMultipleChoice, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_multiple_choice.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz_word = quiz_word
        self.course_words = course_words
        self.mode = mode
        self.max_quiz_words = min(4, len(self.course_words))
        self.settings = Settings()
        self.setup_labels()
        self.setup_reveal_answer_button()
        self.answer_buttons = self.setup_answer_buttons(self.max_quiz_words)
        self.is_correct.connect(self.parent().is_correct_slot)
        self.activate_buttons(True)

    def setup_labels(self):
        # Depends on the mode
        if self.mode == "foreign_to_english":
            self.question_label.setText(self.quiz_word.foreign_word)
        elif self.mode == "english_to_foreign":
            self.question_label.setText(self.quiz_word.translated_word)
        self.question_label.setStyleSheet("font-size: 36px; font-weight: bold")
        self.instructions_label.setStyleSheet("font-size: 20px")

    def setup_answer_buttons(self, max_quiz_words):
        print(max_quiz_words)
        answer_buttons = {}
        for i in range(max_quiz_words):
            answer_buttons[i] = QPushButton("")
            answer_buttons[i].setDefault(False)
            answer_buttons[i].setAutoDefault(False)
            self.answer_button_layout.addWidget(answer_buttons[i])
        return answer_buttons            

    def setup_reveal_answer_button(self):
        self.reveal_answer_button.clicked.connect(self.send_incorrect_signal)
        self.reveal_answer_button.setDefault(False)
        self.reveal_answer_button.setAutoDefault(False)

    def activate_buttons(self, b: bool):
        self.reveal_answer_button.setEnabled(b)

    def send_correct_signal(self):
        self.is_correct.emit(1)

    def send_incorrect_signal(self):
        self.is_correct.emit(0)
