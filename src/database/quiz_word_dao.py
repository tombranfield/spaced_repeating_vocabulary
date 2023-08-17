"""quiz_word_dao.py"""


from src.core.review_time_setter import ReviewTimeSetter
from src.database.database import Database


class QuizWordDAO:
    """
    Acts as an interface to the database in order to perform
    operations for quiz words after learning or reviewing them.
    """
    def __init__(self, db_path=Database.path):
        """Initializes the quiz word data access object"""
        self.db = Database(db_path)

    def set_as_learned(self, quiz_word):
        # using quiz_word.id
        # Sets is_known column to 1
        # increase level by 1
        # set learnt datetime
        # set when to review
        pass

    def add_num_correct(self, quiz_word, num_correct):
        cur_num_correct = self._get_column_value(quiz_word, "num_correct")
        new_num_correct = cur_num_correct + num_correct
        self._update_column_value(quiz_word, "num_correct", new_num_correct)
        
    def add_num_incorrect(self, quiz_word, num_incorrect):
        cur_num_incorrect = self._get_column_value(quiz_word, "num_incorrect")
        new_num_incorrect = cur_num_incorrect + num_incorrect
        self._update_column_value(quiz_word, "num_incorrect", new_num_incorrect)

    def set_word_as_known(self, quiz_word):
        self._update_column_value(quiz_word, "is_known", 1)

    def increase_level(self, quiz_word):
        cur_level = self._get_column_value(quiz_word, "level")
        new_level = cur_level + 1
        self._update_column_value(quiz_word, "level", new_level)

    def set_when_to_review(self, quiz_word):
        # grabs the current level from the database
        # Calls ReviewTimeSetter with that level
        # Calls ReviewTimeSetter's next_review_time method and gets a string
        # Modifies the when_review column with that datetime
        pass

    def _get_column_value(self, quiz_word, column_name):
        query = (
            "SELECT " + column_name + " FROM " + Database.table_name
            + " WHERE rowid = \'" + str(quiz_word.id) + "\'"
        )
        return self.db.result_from_query(query)

    def _update_column_value(self, quiz_word, column_name, new_value):
        query = (
            "UPDATE " + Database.table_name + " set " + column_name
            + " = " + str(new_value) + " where id = \'" + str(quiz_word.id)
            + "\'"
        )
        self.db.connect_and_execute(query)
