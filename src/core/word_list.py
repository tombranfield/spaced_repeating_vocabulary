"""word_list.py"""


from dataclasses import dataclass
from word_pair import WordPair


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

    def is_empty(self) -> bool:
        return False if self._wordpairs else True
        
    



if __name__ == "__main__":

    my_list = WordList("harry potter", "german")

    print(my_list.is_empty())

    print("word_list.py done")
