"""quiz_preview.py"""

from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QLabel



class QuizPreview(QWidget):
    """A widget for the preview screen of the quiz"""

    send_start = pyqtSignal(int)
        
    def __init__(self, words_to_quiz, learn_or_review, parent=None):
        super(QuizPreviewWidget, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "about_window.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.learn_or_review = learn_or_review
        self.words_to_quiz = words_to_quiz

        self.send_start.connect(self.parent().start_slot)
        self.setup_start_button()
        self.add_labels_to_grid()

    def setup_start_button(self):
        start_msg = self.get_start_button_message()
        self.start_button.setText(start_msg)
        self.start_button.clicked.connect(self.send_signal)

    def send_signal(self):
        self.send_start.emit(1)

    def get_start_button_message(self):
        """Creates text for the start button depending on the quiz"""
        if self.learn_or_review == "learn":
            start_msg = "Learn"
        elif self.learn_or_review == "review":
            start_msg = "Review"
        else:
            raise ValueError(learn_or_review must be "learn" or "review")
        if len(self.words_to_quiz) == 1:
            start_msg += " this word"
        else:
            start_msg += " these words"        
        return start_msg

    def add_labels_to_grid(self):
        pass
