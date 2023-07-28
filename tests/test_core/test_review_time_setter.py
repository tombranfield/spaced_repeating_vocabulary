"""
test_review_time_setter.py
"""

import datetime

import pytest

from src.core.review_time_setter import ReviewTimeSetter 


MOCK_DATETIME = datetime.datetime(2023, 12, 25, 9, 0, 30)


@pytest.fixture
def datetime_now(monkeypatch):
    
    class mydatetime:
        @classmethod
        def now(cls):
            return MOCK_DATETIME

    monkeypatch.setattr(datetime, "datetime", mydatetime)


@pytest.fixture
def review_time_setter():
    return ReviewTimeSetter()


def test_patch_datetime(datetime_now):
    assert datetime.datetime.now() == MOCK_DATETIME


def test_current_time(datetime_now, review_time_setter):
    assert review_time_setter.current_time() == "25/12/2023 09:00:30"


def test_returns_correct_review_time_in_desired_format():
    pass    
