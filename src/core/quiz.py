"""quiz.py"""


from src.core.word_pair import WordPair
from src.core.word_selector import WordSelector


class Quiz:
    """
    Represents the quiz
    """
    def __init__(self, id, word_pair: WordPair):
