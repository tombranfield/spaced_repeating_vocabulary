"""test_settings.py"""


from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from src.core.settings import Settings


@pytest.fixture
def settings():
    with TemporaryDirectory() as tmp_dir:
        temp_settings_path = str(Path(tmp_dir)) + "temp_settings.py"
        settings = Settings(temp_settings_path)
        yield settings


def test_initialize_settings_successfully(settings):
    pass


def test_initialize_settings_with_correct_default_values(settings):
    assert settings.is_case_sensitive == True
    assert settings.is_automatic_return == True
    assert settings.max_learn_words == 5
    assert settings.max_review_words == 25


def test_change_and_retrieve_bool_values_successfully(settings):
    settings.is_case_sensitive = False
    settings.is_automatic_return = False
    assert settings.is_case_sensitive == False
    assert settings.is_automatic_return == False


def test_change_and_retrieve_int_values_successfully(settings):
    settings.max_learn_words = 10
    settings.max_review_words = 50
    assert settings.max_learn_words == 10
    assert settings.max_review_words == 50
