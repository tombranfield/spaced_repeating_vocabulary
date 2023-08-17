"""quiz_word_dao.py"""

from datetime import datetime

from src.database.database import Database


class QuizWordDAO:
    """
    Acts as an interface to the database in order to perform
    operations for quiz words after learning or reviewing them.
    """
    def __init__(self, db_path=Database.path):
        """Initializes the quiz word data access object"""
        self.db = Database(db_path)

        self.db.connect_and_execute(query)


    def set_as_learned(self, quiz_word):
        # using quiz_word.id
        # Sets is_known column to 1
        # increase level by 1
        # set learnt datetime
        # set when to review
        pass

    def add_num_correct(self, quiz_word):
        pass

    def add_num_incorrect(self, quiz_word):
        pass

    def increase_level(self, quiz_word):
        pass

    def set_when_to_review(self, quiz_word):
        # grabs the current level from the database
        # Calls ReviewTimeSetter with that level
        # Calls ReviewTimeSetter's new_review_time method
        # Modifies the when_review column with that datetime
        pass
