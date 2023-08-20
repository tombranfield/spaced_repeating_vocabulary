"""quiz_preview.py"""


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

from src.gui.temp_dialog import TempDialog


class QuizPreview(QWidget):
    """A widget for the preview screen of the quiz"""

    send_start = pyqtSignal(int)
        
    def __init__(self, words_to_quiz, learn_or_review, parent=None):
        super(QuizPreview, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_preview.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.learn_or_review = learn_or_review
        self.words_to_quiz = words_to_quiz

        self.send_start.connect(self.parent().start_slot)
        self.setup_start_button()
        self.add_labels_to_grid()
        self.create_temp_dialog()

    def setup_start_button(self):
        start_msg = self.get_start_button_message()
        self.start_button.setText(start_msg)
        self.start_button.setStyleSheet("font-size: 28px; background-color: lime")
        self.start_button.setDefault(True)
        self.start_button.setAutoDefault(True)
        self.start_button.setFocus()
        self.start_button.clicked.connect(self.send_signal)
        self.start_button.setEnabled(False)
        self.start_button.setEnabled(True)

    def send_signal(self):
        self.send_start.emit(1)

    def get_start_button_message(self):
        """Creates text for the start button depending on the quiz"""
        if self.learn_or_review == "learn":
            start_msg = "Learn"
        elif self.learn_or_review == "review":
            start_msg = "Review"
        else:
            raise ValueError("learn_or_review must be 'learn' or 'review'")
        if len(self.words_to_quiz) == 1:
            start_msg += " this word"
        else:
            start_msg += " these words"        
        return start_msg

    def add_labels_to_grid(self):
        for i, quiz_word in enumerate(self.words_to_quiz, 2):
            foreign_label = QLabel(quiz_word.foreign_word)
            translated_label = QLabel(quiz_word.translated_word)
            foreign_label.setStyleSheet(
                "font-weight: bold"
            )
            foreign_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.grid_layout.addWidget(foreign_label, i, 0)
            self.grid_layout.addWidget(translated_label, i, 1)
    
    def create_temp_dialog(self):
        dlg = TempDialog(self)
        dlg.exec_()
