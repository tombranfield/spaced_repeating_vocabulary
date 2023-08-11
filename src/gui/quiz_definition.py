"""quiz_definition.py"""


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


class QuizDefinition(QWidget):
    """A widget for the preview screen of the quiz"""

    send_next = pyqtSignal(int)
        
    def __init__(self, quiz_word, parent=None):
        super(QuizDefinition, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_definition.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz_word = quiz_word

        self.send_next.connect(self.parent().next_slot)
#        self.next_button.clicked.connect(self.send_signal)

    def send_signal(self):
        self.send_next.emit(1)
