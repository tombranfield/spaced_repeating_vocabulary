"""total_stats.py"""


from datetime import datetime

from src.database.database import Database


class TotalStats:
    """
    Responsible for retrieving global statistics from the database
    """
    def __init__(self, db_path=Database.path):
        self.db = Database(db_path)

    def total_words_learnt(self) -> int:
        """Returns the total number of words learnt from all word lists"""
        query = ("SELECT COUNT(*) FROM " + Database.table_name 
                + " WHERE is_known = 1")
        result = self.db.result_from_query(query)
        return result[0][0]

    def total_words_to_review(self) -> int:
        word_lists = self._get_word_lists()
        word_count = 0
        for word_list_name in word_lists:
            query = ("SELECT rowid, when_review FROM " + Database.table_name 
                     + " WHERE is_known = 1 AND word_list_name = \'" 
                     + word_list_name + "\'")
            result = self.db.result_from_query(query)
            for entry in result:
                when_review = datetime.strptime(entry[1], "%d/%m/%Y %H:%M:%S")
                if datetime.now() > when_review:
                    word_count += 1
        return word_count        

    def total_words(self) -> int:
        """Returns the total number of words in the database"""
        query = "SELECT COUNT(rowid) FROM " + Database.table_name
        result = self.db.result_from_query(query)
        return result[0][0]

    def _get_word_lists(self):
        """Returns a list of all the word list names in the database"""
        query = "SELECT DISTINCT word_list_name FROM " + Database.table_name
        result = self.db.result_from_query(query)
        word_lists = [element[0] for element in result]
        return word_lists


if __name__ == "__main__":
    pass
