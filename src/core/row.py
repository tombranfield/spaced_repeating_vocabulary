"""row.py"""


from dataclasses import dataclass


@dataclass
class Row:
    """
    A dataclass that represents a row of data consisting of a foreign word, its
    translation, the language it is in, and the name of the word list it is in.
    """
    foreign_word: str
    translated_word: str
    language: str
    word_list_name: str


if __name__ == "__main__":
    my_row = Row("bullig", "cheap", "german", "harry potter und der stein der weisen")

    print(my_row)
    print(my_row.language)
