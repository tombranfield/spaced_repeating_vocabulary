"""word_pair.py"""


from dataclasses import dataclass


@dataclass
class WordPair:
    """
    A dataclass that represents the pair of a foreign word with its translation
    """
    foreign_word: str
    translated_word: str


if __name__ == "__main__":
    pass
