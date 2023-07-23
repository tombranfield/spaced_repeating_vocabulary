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
