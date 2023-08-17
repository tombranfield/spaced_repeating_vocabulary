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

    def set_as_learnt(self, quiz_word):
        self.set_word_as_known(quiz_word)
        self.increase_level(quiz_word)
        self.set_when_to_review(quiz_word)

    def finished_reviewing(self, quiz_word):
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

    def reset_level(self, quiz_word):
        self._update_column_value(quiz_word, "level, 1)

    def set_when_to_review(self, quiz_word):
        cur_level = self._get_column_value(quiz_word, "level")
        review_time_setter = ReviewTimeSetter(cur_level)
        next_review_time = review_time_setter.next_review_time()
        self._update_column_value(quiz_word, "when_review", next_review_time)

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
