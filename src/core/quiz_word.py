"""quiz_word.py"""


from src.core.quiz_stack import QuizStack
from src.core.word_pair import WordPair


class QuizWord:
    """
    Represents a word that is currently being learned or reviewed
    """
    def __init__(self, id, word_pair: WordPair, quiz_type="learn"):
        self._id = id
        self._foreign_word = word_pair.foreign_word
        self._translated_word = word_pair.translated_word
        self.num_correct = 0
        self.num_incorrect = 0
        self.is_review_correct = None
        self.quiz_type = quiz_type
        self.quiz_stack = QuizStack(self.quiz_type)
        self.progress_score = 0
        self.max_progress_score = self.quiz_stack.length()

        #TODO
    def print_items(self):
        print(
            "Quiz stack of", self._foreign_word, " is now ",
            self.quiz_stack.items
        )

    @property
    def id(self):
        return self._id

    @property
    def foreign_word(self):
        return self._foreign_word

    @property
    def translated_word(self):
        return self._translated_word

    def get_next_quiz(self):
        return self.quiz_stack.next_quiz()

    def set_next(self):
        self.progress_score += 1
        self.quiz_stack.correct()

    def set_correct(self):
        self.num_correct += 1
        self.progress_score += 1
        self.quiz_stack.correct()

    def set_incorrect_multiple_quiz(self):
        self.num_incorrect += 1
        if self.quiz_type == "learn":
            self.max_progress_score += 1
            self.quiz_stack.incorrect_multiple_quiz()
        if self.quiz_type == "review" and self.is_review_correct is None:
            self.is_review_correct = False

    def set_incorrect_typing_quiz(self):
        self.num_incorrect += 1
        self.max_progress_score += 2
        self.quiz_stack.incorrect_typing_quiz()
        if self.quiz_type == "review" and self.is_review_correct is None:
            self.is_review_correct = False

    def is_quizzing_finished(self):
        return self.quiz_stack.is_finished()

    
