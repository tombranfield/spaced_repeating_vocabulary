"""quiz_multiple_choice.py"""


from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
)

from src.core.settings import Settings


class QuizMultipleChoice(QWidget):
    """A widget for a typing test in the quiz"""
    is_correct = pyqtSignal(int)
        
    def __init__(self, quiz_word, parent=None):
        super(QuizTypingTest, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_multiple_choice.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz_word = quiz_word
        self.settings = Settings()
        self.setup_labels()
        self.setup_reveal_answer_button()
#       self.answer_buttons = self.setup_answer_buttons()
        self.is_correct.connect(self.parent().is_correct_slot)
        self.activate_buttons(True)

    def setup_labels(self):
        self.foreign_word_label.setText(self.quiz_word.foreign_word)
        self.foreign_word_label.setStyleSheet("font-size: 36px; font-weight: bold")
        self.instructions_label.setStyleSheet("font-size: 20px")

    def setup_reveal_answer_button(self):
        self.reveal_answer_button.clicked.connect(self.send_incorrect_signal)
        self.reveal_answer_button.setDefault(False)
        self.reveal_answer_button.setAutoDefault(False)

    def activate_buttons(self, b: bool):
        self.answer_entry.setEnabled(b)
        self.reveal_answer_button.setEnabled(b)

    def send_correct_signal(self):
        self.is_correct.emit(1)

    def send_incorrect_signal(self):
        self.is_correct.emit(0)
