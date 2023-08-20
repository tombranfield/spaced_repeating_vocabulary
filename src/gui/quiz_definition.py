"""quiz_definition.py"""


from pathlib import Path

from PyQt5 import uic

from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
    QEvent,
    QTimer,
)
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
)

from src.core.settings import Settings
from src.gui.temp_dialog import TempDialog


class QuizDefinition(QWidget):
    """A widget for the definition screen of the quiz"""

    send_next = pyqtSignal(int)
        
    def __init__(self, quiz_word, is_typing=True, parent=None):
        super(QuizDefinition, self).__init__(parent=parent)
        uic.loadUi(str(Path(__file__).parents[0] / "quiz_definition.ui"), self)
        stylesheet_path = str(Path(__file__).parents[0] / "stylesheet.css")
        self.setStyleSheet(open(stylesheet_path).read())

        self.quiz_word = quiz_word
        self.settings = Settings()
        self.setup_labels()
        self.setup_definition_entry()
        self.setup_next_button()
        self.is_typing = is_typing
        self.show_typing_widgets(self.is_typing)            
        self.activate_buttons(True)
        self.next_button.installEventFilter(self)
        self.create_temp_dialog()

    def eventFilter(self, source, event):
#        if source == self.next_button:
#            print("hi") # works
        if event.type() == QEvent.KeyPress:
#            print("keypress") # works
#            print(event.type()) # prints 6
            key = event.key()
#            print(key)
            if key != Qt.Key_Return:
#                print("not enter, ignored")
                return True
            else:
#                print("pressed return")
                pass
        return False
    
    def setup_labels(self):
        self.foreign_word_label.setText(self.quiz_word.foreign_word)
        self.translated_word_label.setText(self.quiz_word.translated_word)
        self.translated_word_label.setStyleSheet("font-size: 28px")
        self.instructions_label.setStyleSheet("font-size: 20px")

    def show_typing_widgets(self, is_typing):
        """Shows the instructions and definition entry widgets"""
        if is_typing:
            self.instructions_label.show()
            self.definition_entry.show()
            self.next_button.hide()
            self.definition_entry.setEnabled(True)
            self.next_button.setEnabled(False)
            self.definition_entry.setFocus()
        else:
            self.instructions_label.hide()
            self.definition_entry.hide()
            self.next_button.show()
            self.definition_entry.setEnabled(False)
            self.next_button.setEnabled(True)
            self.next_button.setFocus()
            
    def setup_next_button(self):
        self.send_next.connect(self.parent().next_slot)
        self.next_button.clicked.connect(self.send_signal)
        self.next_button.setDefault(True)
        self.next_button.setAutoDefault(True)

    def setup_definition_entry(self):
        self.definition_entry.setPlaceholderText(self.quiz_word.foreign_word)
        self.definition_entry.returnPressed.connect(
            self.definition_entry_return_pressed
        )
        self.definition_entry.textEdited.connect(
            self.definition_entry_text_edited
        )

    def definition_entry_return_pressed(self):
        current_text = self.definition_entry.text()
        if current_text == self.quiz_word.foreign_word:
            self.definition_entry.setStyleSheet("background: lime")
            self.definition_entry.setEnabled(False)
            QTimer.singleShot(1000, self.send_signal)
            #self.send_signal()

    def definition_entry_text_edited(self, answer_input):
        if self.settings.is_automatic_return:
            if not self.settings.is_case_sensitive:
                answer_input = answer_input.lower()
            if answer_input == self.quiz_word.foreign_word:
                self.definition_entry.setStyleSheet("background: lime")
                self.definition_entry.setEnabled(False)
                QTimer.singleShot(1000, self.send_signal)
                #self.send_signal()

    def activate_buttons(self, b: bool):
        self.definition_entry.setEnabled(b)
        self.next_button.setEnabled(b)

    def send_signal(self):
        self.send_next.emit(1)

    def create_temp_dialog(self):
        dlg = TempDialog(self)
        dlg.exec_()
