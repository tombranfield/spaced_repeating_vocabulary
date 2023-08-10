"""quiz.py"""


from pathlib import Path
from typing import Literal

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


_QUIZ_TYPE = Literal["learn", "review"]


class Quiz(QDialog):
    """Quiz for learning or reviewing words"""
    def __init__(self, learn_or_review: _QUIZ_TYPE, parent=None):
        super().__init__(parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz = learn_or_review

        self.quit_button.clicked.connect(self.close_window)       
    


    def close_window(self):
        self.close()
