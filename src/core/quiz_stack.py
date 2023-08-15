"""quiz_stack.py"""


class QuizStack:
    """
    Represents the sequence of different tests during a quiz
    """
    learn_sequence  = (
        "typing_test_quiz",
        "english_to_foreign_multiple_quiz",
        "foreign_to_english_multiple_quiz",
        "typing_quiz",
        "foreign_to_english_multiple_quiz",
        "english_to_foreign_multiple_quiz",
        "word_definition",
        )
    review_sequence = (
        "typing_quiz",
    )
    
    def __init__(self, quiz_type):
        self.quiz_type = quiz_type
        if self.quiz_type == "learn":
            self.items = list(learn_sequence)
        elif self.quiz_type == "review":
            self.items = list(review_sequence)

    def next_quiz(self):
        return self.items[-1] 

    def correct(self):
        self.items.pop()

    def incorrect_multiple_quiz(self):
        if self.quiz_type == "learn":
            self.items.append("word_definition")

    def incorrect_typing_quiz(self):
        if self.quiz_type == "learn":
            self.items.append("word_definition_typing")
            self.items.append("english_to_foreign_multiple_quiz")
        elif self.quiz_type == "review":
            self.items.append("foreign_to_english_multiple_quiz")
            self.items.append("english_to_foreign_multiple_quiz")

    def is_finished(self) -> bool:
        return True if not self.items else False
