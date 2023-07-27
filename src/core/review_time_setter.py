"""
review_time_setter.py
"""

import sys
import datetime


class ReviewTimeSetter:
    """
    Responsible for giving words the next time to be reviewed
    """
    def __init__(self, new_level):
        self_new_level = new_level
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
        added_hours = self.get_num_hours_from_level()

    def _extra_hours_for_level(self):
        pass

    def _get_datetime_string(self, datetime):
        pass
