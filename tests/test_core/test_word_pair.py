"""test_word_pair.py"""

from src.core.word_pair import WordPair

import pytest


@pytest.fixture
def word_pair():
    foreign_word = "bullig"
    translated_word = "cheap"
    return WordPair(foreign_word, translated_word)



def test_can_extract_foreign_word_from_word_pair(word_pair):
    assert word_pair.foreign_word == "bullig"


def test_can_extract_translated_word_from_word_pair(word_pair):
    assert word_pair.translated_word == "cheap"
