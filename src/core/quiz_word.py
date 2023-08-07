"""quiz_word.py"""


from src.core.word_pair import WordPair


class QuizWord:
    """
    Represents a word that is currently being learned or reviewed
    """
    def __init__(self, id, word_pair: WordPair):
        self._id = id
        self._foreign_word = word_pair.foreign_word
        self._translated_word = word_pair.translated_word
        self.progress_score = 0
        self.num_correct = 0
        self.num_incorrect = 0

    @property
    def id(self):
        return self._id

    @property
    def foreign_word(self):
        return self._foreign_word

    @property
    def translated_word(self):
        return self._translated_word
