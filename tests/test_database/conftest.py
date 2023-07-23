"""
conftest.py
"""

import pytest

from src.core.row import Row


@pytest.fixture
def row_of_data():
    row = Row("bullig", "cheap", "german", 
              "Harry Potter und der Stein der Weisen")
    return row


@pytest.fixture
def rows_of_data():
    row_1 = Row("bonjour", "hello", "french", "basic words")
    row_2 = Row("merci", "thank you", "french", "basic words")
    row_3 = Row("au revoir", "goodbye", "french", "basic words")
    return (row_1, row_2, row_3)
