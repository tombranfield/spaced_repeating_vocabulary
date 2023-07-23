"""
Testing row_dao.py
"""

from pathlib import Path
import pytest
from tempfile import TemporaryDirectory

from src.core.row import Row
from src.database.row_dao import RowDAO


@pytest.fixture
def row_of_data():
    row = Row("bullig", "cheap", "german",
              "Harry Potter und der Stein der Weisen")
