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


def test_export_word_pairs_successfully(word_list, word_pairs):
    assert word_list.word_pairs == word_pairs


def test_is_empty_returns_true_for_empty_list(empty_word_list):
    assert empty_word_list.is_empty() == True


def test_is_empty_returns_false_for_non_empty_word_list(word_list):
    assert word_list.is_empty() == False


def test_export_word_pairs_of_empty_list_gives_empty_tuple(empty_word_list):
    assert empty_word_list.word_pairs == ()


def test_foreign_words_are_successfully_exported(word_list):
    print(word_list.foreign_words())
    assert word_list.foreign_words() == ("bullig", "danke", "hallo")


def test_can_add_word_pair(empty_word_list):
    word_pair = WordPair("danke", "thank you")
    empty_word_list.add_word_pair(word_pair)
    assert empty_word_list.word_pairs == (word_pair,)


def test_number_of_words_in_empty_list_is_zero(empty_word_list):
    assert empty_word_list.num_words() == 0


def test_correct_number_of_held_words_is_returned(word_list):
    assert word_list.num_words() == 3


def test_cannot_make_word_list_with_no_name():
    with pytest.raises(ValueError):
        no_name_list = WordList("", "German")


def test_cannot_make_word_list_with_no_language():
    with pytest.raises(ValueError):
        no_lang_list = WordList("My Word List", "")


