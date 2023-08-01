"""total_stats.py"""


from datetime import datetime

from src.database.database import Database


class TotalStats:
    """
    Responsible for retrieving global statistics from the database
    """
    def __init__(self, db_path=Database.path):
        self.db = Database(db_path)
#        self.table_name = Database.table_name
        self.table_name = "master_wordlist"

    def total_words_learnt(self) -> int:
        """Returns the total number of words learnt from all word lists"""
#        query = ("SELECT COUNT(*) FROM " + Database.table_name 
        query = ("SELECT COUNT(*) FROM " + self.table_name
                + " WHERE is_known = 1")
        result = self.db.result_from_query(query)
        return result[0][0]

    def total_words_to_review(self) -> int:
        # Get a list of word_lists using SQL DISTINCT
        word_lists = self._get_word_lists()
        word_count = 0
        for word_list_name in word_lists:
            query = ("SELECT rowid, when_review WHERE is_known = 1 AND "
                    + "list_name = \'" + word_list_name + "\'")
            result = self.db.result_from_query(query)
            for entry in result:
                when_review = datetime.strptime(entry[2], "%d/%m/%Y %H:%M:%$
                if datetime.now() > when_review:
                    word_count += 1
        return word_count        

    def total_words(self) -> int:
        """Returns the total number of words in the database"""
        query = "SELECT COUNT(*) FROM " + self.table_name
        result = self.db.result_from_query(query)
        return result[0][0]

    def _get_word_lists(self):
        """Returns a list of all the word list names in the database"""
#        query = "SELECT DISTINCT word_list_name FROM " + Database.table_name
        query = "SELECT DISTINCT list_name FROM " + self.table_name
        result = self.db.result_from_query(query)
        word_lists = [element[0] for element in result]
        return word_lists


if __name__ == "__main__":
    
    total_stats = TotalStats("harry_potter.db")

    print("Total words:", total_stats.total_words())
    print("Total words learned:", total_stats.total_words_learnt())
    print("Word lists:", total_stats._get_word_lists())
    print("Total words to review:")
