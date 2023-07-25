"""word_list.py"""


from dataclasses import dataclass
from wordpair import WordPair


class WordList:
    """
    A class that represents a word list.
    """
    def __init__(self, word_list_name: str, language: str, wordpairs: WordPair = None):
        """Initializes the word list"""
        self._word_list_name = word_list_name
        self._language = language
        self._wordpairs = wordpairs

    @property
    def word_list_name(self):
        return self._word_list_name

    @property
    def language(self):
        return self._language
    



if __name__ == "__main__":
    print("word_list.py done")
