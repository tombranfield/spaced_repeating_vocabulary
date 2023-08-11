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


class QuizTypingTest(QWidget):
    """A widget for the preview screen of the quiz"""

    is_correct = pyqtSignal(int)
        
    def __init__(self, quiz_word, parent=None):
        super(QuizTypingTest, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_typing_test.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz_word = quiz_word
        self.settings = Settings()
        self.setup_labels()
        self.setup_answer_entry()
        self.setup_reveal_answer_button()
        self.is_correct.connect(self.parent().is_correct_slot)
        self.activate_buttons(True)

    def setup_labels(self):
        self.translated_word_label.setText(self.quiz_word.translated_word)
        self.translated_word_label.setStyleSheet("font-size: 36px; font-weight: bold")
        self.instructions_label.setStyleSheet("font-size: 20px")

    def setup_definition_entry(self):
        self.answer_entry.setPlaceholderText(self.quiz_word.foreign_word)
        self.answer_entry.returnPressed.connect(
            self.answer_entry_return_pressed
        )
        self.answer_entry.returnPressed.connect(
            self.answer_entry_text_edited
        )

    def setup_reveal_answer_button(self):
        self.reveal_answer_button.clicked.connect(self.send_incorrect_signal)
        self.reveal_answer_button.setDefault(False)
        self.reveal_answer_button.setAutoDefault(False)

    def answer_entry_return_pressed(self):
        current_text = self.answer_entry.text()
        print("typed", current_text)
        if current_text == self.quiz_word.foreign_word:
            self.send_signal()

    def answer_entry_text_edited(self):
        # If automatic return
            # If is case sensitive
        pass

    def activate_buttons(self, b: bool):
        self.answer_entry.setEnabled(b)
        self.reveal_answer_button.setEnabled(b)

    def set_answer_entry_background(self, is_correct=True):
        if is_correct:
            pass
        else:
            pass

    def reset_answer_entry_background(self):
        pass

    def send_correct_signal(self):
        self.is_correct.emit(1)

    def send_incorrect_signal(self):
        print("sent incorrect signal")
        self.is_correct.emit(0)
