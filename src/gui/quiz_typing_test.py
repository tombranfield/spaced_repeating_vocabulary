"""quiz_typing_test.py"""


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


class QuizDefinition(QWidget):
    """A widget for the preview screen of the quiz"""

    is_correct = pyqtSignal(int)
        
    def __init__(self, quiz_word, parent=None):
        super(QuizDefinition, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_typing_test.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz_word = quiz_word
        self.setup_labels()
        self.setup_definition_entry()
        self.setup_reveal_answer_button()

    def setup_labels(self):
        self.translated_word_label.setText(self.quiz_word.translated_word)
        self.translated_word_label.setStyleSheet("font-size: 28px")
        self.instructions_label.setStyleSheet("font-size: 20px")

    def setup_definition_entry(self):
        self.definition_entry.setPlaceholderText(self.quiz_word.foreign_word)
        self.definition_entry.returnPressed.connect(
            self.definition_entry_return_pressed
        )

    def setup_reveal_answer_button(self):
        self.send_next.connect(self.parent().next_slot)
        self.reveal_answer_button.clicked.connect(self.send_signal)
        self.reveal_answer_button.setDefault(False)
        self.reveal_answer_button.setAutoDefault(False)
        self.reveal_answer_button.setStyleSheet("background: gray")

    def definition_entry_return_pressed(self):
        current_text = self.definition_entry.text()
        print("typed", current_text)
        if current_text == self.quiz_word.foreign_word:
            self.send_signal()

    def send_correct_signal(self):
        self.is_correct.emit(1)

    def send_incorrect_signal(self):
        self.is_correct.emit(0)
