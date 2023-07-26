"""test_word_list.py"""

from src.core.word_list import WordList

import pytest


@pytest.fixture
def word_list():
    words = (WordPair("bullig", "cheap"),
             WordPair("danke", "thank you")
             WordPair("hallo", "hello"))
    word_list = WordList("My Word List", "German", words)
    return word_list
