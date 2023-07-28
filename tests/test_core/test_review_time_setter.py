"""
test_review_time_setter.py
"""

import datetime

import pytest

from src.core.review_time_setter import ReviewTimeSetter 


MOCK_DATETIME = datetime.datetime(2023, 12, 25, 9, 0, 30)


@pytest.fixture
def datetime_mock(monkeypatch):
    
    class mydatetime:
        @classmethod
        def now(cls):
            return MOCK_DATETIME

    monkeypatch.setattr(datetime, "datetime", mydatetime)


@pytest.fixture
def review_time_setter():
    return ReviewTimeSetter()


def test_patch_datetime(datetime_mock):
    assert datetime.datetime.now() == MOCK_DATETIME


def test_current_time(datetime_mock, review_time_setter):
    assert review_time_setter.current_time() == "25/12/2023 09:00:30"


def test_returns_correct_review_time_level_1(datetime_mock):
    review_time_setter = ReviewTimeSetter()
    next_review_time = review_time_setter.next_review_time()    
    assert next_review_time == "25/12/2023 13:00:30"


def test_returns_correct_review_time_level_13(datetime_mock):
    review_time_setter = ReviewTimeSetter(13)
    next_review_time = review_time_setter.next_review_time()
    assert next_review_time == "22/06/2024 09:00:30"


def test_negative_input_level_classed_as_error():
    with pytest.raises(ValueError):
        review_time_setter = ReviewTimeSetter(-10)


def test_non_integer_input_level_classed_as_error():
    with pytest.raises(ValueError):
        review_time_setter = ReviewTimeSetter("hi!")
