"""quiz_multiple_choice.py"""


from pathlib import Path
import random
import time

from PyQt5 import uic
from PyQt5.QtCore import (
    pyqtSignal,
    QEvent,
    Qt,
    QTimer,
)
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
)

from src.core.settings import Settings
from src.gui.temp_dialog import TempDialog


class QuizMultipleChoice(QWidget):
    """A widget for a typing test in the quiz"""
    is_correct = pyqtSignal(int)
        
    def __init__(self, quiz_word, course_words, quiz_type, parent=None):
        super(QuizMultipleChoice, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_multiple_choice.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz_word = quiz_word
        self.course_words = course_words
        self.quiz_type = quiz_type
        self.settings = Settings()
        self.setup_labels()
        self.setup_reveal_answer_button()

        self.max_quiz_words = min(4, len(self.course_words))
        self.correct_answer_index = random.randint(0, self.max_quiz_words - 1)
        self.answer_buttons = self.create_answer_buttons(self.max_quiz_words)
        self.is_correct.connect(self.parent().is_correct_slot)
        self.answer_buttons[0].installEventFilter(self)
        self.activate_buttons(True)
        self.reset_answer_buttons_background()
        self.reveal_answer_button.installEventFilter(self)
        self.create_temp_dialog()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1 and self.answer_buttons[0]:
            self.answer_buttons[0].click()
        if event.key() == Qt.Key_2 and self.answer_buttons[1]:
            self.answer_buttons[1].click()
        if event.key() == Qt.Key_3 and self.answer_buttons[2]:
            self.answer_buttons[2].click()
        if event.key() == Qt.Key_4 and self.answer_buttons[3]:
            self.answer_buttons[3].click()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key not in [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4]:
                return True
        return False

    def setup_labels(self):
        if self.quiz_type == "foreign_to_english":
            self.question_label.setText(self.quiz_word.foreign_word)
        elif self.quiz_type == "english_to_foreign":
            self.question_label.setText(self.quiz_word.translated_word)
        self.question_label.setStyleSheet("font-size: 36px; font-weight: bold")
        self.instructions_label.setStyleSheet("font-size: 20px")

    def create_answer_buttons(self, max_quiz_words):
        answer_buttons = {}
        for i in range(max_quiz_words):
            answer_buttons[i] = QPushButton("")
            answer_buttons[i].setDefault(False)
            answer_buttons[i].setAutoDefault(False)
            if i == self.correct_answer_index:
                answer_buttons[i].setText(self.get_correct_button_text()) 
                answer_buttons[i].clicked.connect(self.sent_correct_answer)
            else:
                answer_buttons[i].setText(self.get_incorrect_button_text())
                answer_buttons[i].clicked.connect(self.sent_incorrect_answer)
            self.answer_button_layout.addWidget(answer_buttons[i])
        return answer_buttons            

    def get_correct_button_text(self):
        if self.quiz_type == "english_to_foreign":
            return self.quiz_word.foreign_word
        elif self.quiz_type == "foreign_to_english":
            return self.quiz_word.translated_word

    def get_incorrect_button_text(self):
        while True:
            random_word = random.choice(self.course_words)
            if random_word.foreign_word != self.quiz_word.foreign_word:
                break
        if self.quiz_type == "english_to_foreign":
            return random_word.foreign_word
        elif self.quiz_type == "foreign_to_english":
            return random_word.translated_word                

    def setup_reveal_answer_button(self):
        self.reveal_answer_button.clicked.connect(self.sent_incorrect_answer)
        self.reveal_answer_button.setDefault(False)
        self.reveal_answer_button.setAutoDefault(False)

    def sent_correct_answer(self):
        self.set_answer_buttons_background()
        self.activate_buttons(False)
        QTimer.singleShot(1000, self.send_correct_signal)

    def sent_incorrect_answer(self):
        self.set_answer_buttons_background()
        self.activate_buttons(False)
        QTimer.singleShot(1000, self.send_incorrect_signal)

    def activate_buttons(self, b: bool):
        for i in range(self.max_quiz_words):
            self.answer_buttons[i].setEnabled(b)
        self.reveal_answer_button.setEnabled(b)

    def reset_answer_buttons_background(self):
        for key in self.answer_buttons:
            self.answer_buttons[key].setStyleSheet("background: white")

    def set_answer_buttons_background(self):
        for key in self.answer_buttons:
            if key == self.correct_answer_index:
                self.answer_buttons[key].setStyleSheet("background: lime")
            else:
                self.answer_buttons[key].setStyleSheet("background: darkred")

    def send_correct_signal(self):
        self.is_correct.emit(1)

    def send_incorrect_signal(self):
        self.is_correct.emit(0)

    def create_temp_dialog(self):
        dlg = TempDialog(self)
        dlg.exec_()
