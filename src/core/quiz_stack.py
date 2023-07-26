"""quiz_stack.py"""


class QuizStack:
    """
    Represents the sequence of different tests during a quiz
    """
    def __init__(self):
        self.items = [
            "typing_test_quiz",
            "english_to_foreign_multiple_quiz",
            "foreign_to_english_multiple_quiz",
            "typing_quiz",
            "foreign_to_english_multiple_quiz",
            "english_to_foreign_multiple_quiz",
            "word_defintion",
        ]

    def correct(self):
        self.items.pop()

    def incorrect_multiple_quiz(self):
        self.items.append("word_definition")

    def incorrect_typing_quiz(self):
        self.items.append("word_definition_typing")
        self.items.append("engish_to_foreign_multiple_quiz")

    def is_finished(self) -> bool:
        return True if not self.items else False



if __name__ == "__main__":
    learn_stack = QuizStack()
    for i in range(6):
        learn_stack.correct()
    print(learn_stack.is_finished())

    learn_stack.correct()
    print(learn_stack.is_finished())
