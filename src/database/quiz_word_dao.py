"""quiz_word_dao.py"""


from src.core.review_time_setter import ReviewTimeSetter
from src.database.database import Database


class QuizWordDAO:
    """
    Acts as an interface to the database in order to perform
    operations for quiz words after learning or reviewing them.
    """
    def __init__(self, quiz_word, db_path=Database.path):
        """Initializes the quiz word data access object"""
        self.db = Database(db_path)
        self.quiz_word = quiz_word

    def set_as_learnt(self):
        self.set_word_as_known()
        self.set_when_to_review()

    def finished_reviewing(self):
        if self.quiz_word.was_review_correct:
            self.increase_level()
        else:
            self.reset_level()
        self.set_when_to_review()

    def add_num_correct(self, num_correct):
        cur_num_correct = self._get_column_value("num_correct")
        new_num_correct = cur_num_correct + num_correct
        self._update_column_value("num_correct", new_num_correct)
        
    def add_num_incorrect(self, num_incorrect):
        cur_num_incorrect = self._get_column_value("num_incorrect")
        new_num_incorrect = cur_num_incorrect + num_incorrect
        self._update_column_value("num_incorrect", new_num_incorrect)

    def set_word_as_known(self):
        self._update_column_value("is_known", 1)

    def increase_level(self):
        cur_level = self._get_column_value("level")
        new_level = cur_level + 1
        self._update_column_value("level", new_level)

    def reset_level(self):
        self._update_column_value("level", 1)

    def set_when_to_review(self):
        cur_level = self._get_column_value("level")
        review_time_setter = ReviewTimeSetter(cur_level)
        next_review_time = review_time_setter.next_review_time()
        self._update_column_value("when_review", next_review_time)

    def _get_column_value(self, column_name):
        query = (
            "SELECT " + column_name + " FROM " + Database.table_name
            + " WHERE rowid = \'" + str(self.quiz_word.id) + "\'"
        )
        return self.db.result_from_query(query)[0][0]

    def _update_column_value(self, column_name, new_value):
        query = (
            "UPDATE " + Database.table_name + " set " + column_name
            + " = '" + str(new_value) + "' where rowid = \'" 
            + str(self.quiz_word.id) + "\'"
        )
        self.db.connect_and_execute(query)
