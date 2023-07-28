"""
review_time_setter.py
"""

import sys
import datetime


class ReviewTimeSetter:
    """
    Responsible for determining the next time a word should be reviewed
    """
    def __init__(self, level=1):
        self._level = level
        self._verify_valid_level(self._level)
        self.level_hours_dict = {
            1 : 4,
            2 : 24,
            3 : 144,
            4 : 288,
            5 : 576,
            6 : 1152,
            7 : 2304,
            8 : 4320
            }

    def current_time(self):
        return self._get_datetime_string(datetime.datetime.now())

    def next_review_time(self):
        """
        Returns a string representing the next review time for a word
        """
        added_hours = self._number_hours_until_review()
        now = datetime.datetime.now()
        review_time = now + datetime.timedelta(hours = added_hours)
        return self._get_datetime_string(review_time)

    def _number_hours_until_review(self):
        """Returns how many hours in the future a word should be reviewed"""
        if self._level < 9:
            return self.level_hours_dict[self._level]
        else:
            # Time between reviews should be no longer than 180 days
            return self.level_hours_dict[8]

    def _get_datetime_string(self, datetime):
        """Returns a formatted string for a given datetime object"""
        return datetime.strftime("%d/%m/%Y %H:%M:%S")

    def _verify_valid_level(self, level):
        """Verifies whether the supplied level is valid"""
        error_message = "Entered level must be a positive integer"
        if not isinstance(level, int):
            raise ValueError(error_message)
        if level < 1:
            raise ValueError(error_message)
