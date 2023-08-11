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

        #TODO for casual testing
        print("\t\t\t", self.quiz_word.foreign_word)
        print("\t\t", self.settings.is_case_sensitive)
        print("\t\t", self.settings.is_automatic_return)

    def setup_labels(self):
        self.translated_word_label.setText(self.quiz_word.translated_word)
        self.translated_word_label.setStyleSheet("font-size: 36px; font-weight: bold")
        self.instructions_label.setStyleSheet("font-size: 20px")

    def setup_answer_entry(self):
        # TODO remove below line, is for casual testing
        self.answer_entry.setPlaceholderText(self.quiz_word.foreign_word)
        self.answer_entry.returnPressed.connect(
            self.answer_entry_return_pressed
        )
        self.answer_entry.textEdited.connect(
            self.answer_entry_text_edited
        )

    def setup_reveal_answer_button(self):
        self.reveal_answer_button.clicked.connect(self.send_incorrect_signal)
        self.reveal_answer_button.setDefault(False)
        self.reveal_answer_button.setAutoDefault(False)

    def answer_entry_return_pressed(self):
        current_text = self.answer_entry.text()
        if not self.settings.is_case_sensitive:
            current_text = current_text.lower()
        if current_text == self.quiz_word.foreign_word:
            # set background
            self.send_correct_signal()
        else:
            # set background
            self.send_incorrect_signal()
        self.activate_buttons(False)

    def answer_entry_text_edited(self, answer_input):
        """
        if self.settings.is_automatic_return:
            if not self.settings.is_case_sensitive:
                answer_input = answer_input.lower()
            print(answer_input)
            if answer_input == self.quiz_word.foreign_word:
                self.send_correct_signal()
        """

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
        print("\t\t", "sent correct signal")
        self.is_correct.emit(1)

    def send_incorrect_signal(self):
        print("\t\t", "sent incorrect signal")
        self.is_correct.emit(0)
