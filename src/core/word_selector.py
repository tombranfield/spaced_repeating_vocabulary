"""word_selector.py"""


from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.database.database import Database


class WordSelector:
    """
    Responsible for choosing words to learn or review from the database.
    """
    def __init__(self, word_list_name):
        self.word_list_name = word_list_name

    def words_to_learn(self) -> WordList:
        """Returns a word list containing the words to learn"""
        returns 


    def words_to_review(self) -> WordList:
        """Returns a word list containing the words to review"""



    def _language_of_list(self):
        """Gets the language of the word list"""
