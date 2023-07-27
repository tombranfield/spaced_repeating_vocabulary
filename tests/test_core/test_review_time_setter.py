"""
test_review_time_setter.py
"""

import datetime


from src.core.review_time_setter import ReviewTimeSetter 


FAKE_TIME = datetime.datetime(2023, 12, 25, 9, 0, 30)


@pytest.fixture
def datetime_now(monkeypatch):
    
    class mydatetime:
        @classmethod
        def now(cls):
            return FAKE_TIME

    monkeypatch.setattr(datetime. "datetime", mydatetime)




def test_patch_datetime(datetime_now):
    assert datetime.datetime.now() == FAKE_TIME



def test_returns_current_time_in_desired_format(self):
    review_time_setter = ReviewTimeSetter()
    current_time = review_time_setter.current_time()
    
