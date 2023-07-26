"""word_list.py"""


from dataclasses import dataclass
from src.core.word_pair import WordPair


class WordList:
    """
    A class that represents a word list.
    """
    def __init__(self, word_list_name: str, language: str, word_pairs: WordPair =()):
        """Initializes the word list"""
        self._name = word_list_name
        self._language = language
        self._word_pairs = word_pairs
        self._verify_has_name_and_language()

    @property
    def name(self):
        return self._name

    @property
    def language(self):
        return self._language

    @property
    def word_pairs(self):
        return self._word_pairs

    def foreign_words(self):
        foreign_words = ()
        for word_pair in self._word_pairs:
            foreign_words += (word_pair.foreign_word,)
        return foreign_words

    def num_words(self) -> int:
        return len(self._word_pairs)

    def add_word_pair(self, word_pair: WordPair):
        """Add a WordPair to the word list"""   
        self._word_pairs += (word_pair,)

    def is_empty(self) -> bool:
        return False if self._word_pairs else True
        
    def _verify_has_name_and_language(self) -> bool:
        """Returns whether a word list has a name and language"""    
        if not self._name or not self._language:
            raise ValueError("Need to supply a name and language for the word list")


if __name__ == "__main__":

    wordpair_1 = WordPair("bullig", "cheap")
    wordpair_2 = WordPair("danke", "thank you")
    wordpairs = (wordpair_1, wordpair_2)

    my_list = WordList("harry potter", "german", wordpairs)
    
    print(my_list._word_pairs)

    broken_list = WordList("", 'german', wordpairs)


    print("word_list.py done")
