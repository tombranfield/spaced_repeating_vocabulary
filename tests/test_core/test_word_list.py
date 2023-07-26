"""test_word_list.py"""

from src.core.word_list import WordList
from src.core.word_pair import WordPair

import pytest


@pytest.fixture
def word_pairs():
    word_pairs = (WordPair("bullig", "cheap"),
             WordPair("danke", "thank you"),
             WordPair("hallo", "hello"))
    return word_pairs

@pytest.fixture
def word_list(word_pairs):
    word_list = WordList("My Word List", "German", word_pairs)
    return word_list


@pytest.fixture
def empty_word_list():
    word_list = WordList("My Empty Word List", "German")
    return word_list


def test_get_name_of_list(word_list):
    assert word_list.name == "My Word List"


def test_get_language_of_list(word_list):
    assert word_list.language == "German"


def test_export_word_pairs_successfulyy(word_list, word_pairs):
    assert word_list.word_pairs == word_pairs


def test_is_empty_returns_true_for_empty_list(empty_word_list):
    assert empty_word_list.is_empty() == True


def test_is_empty_returns_false_for_word_list_with_entries(word_list):
    assert word_list.is_empty() == False


def test_export_word_pairs_of_empty_list_gives_empty_tuple(empty_word_list):
    assert empty_word_list.word_pairs == ()
