"""word_pair.py"""


from dataclasses import dataclass


@dataclass
class WordPair:
    """
    A dataclass consisting of a foreign word with its translation
    """
    foreign_word: str
    translated_word: str


if __name__ == "__main__":
    
    my_pair = WordPair("bullig", "cheap")

    print(my_pair.foreign_word)
    print(my_pair.translated_word)
