"""global_stats.py"""


from src.database.database import Database


class GlobalStats:
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
        return result

    def total_words_to_review(self) -> int:
        pass

    def total_words(self) -> int:
        """Returns the total number of words in the database"""
        pass


if __name__ == "__main__":
    global_stats = GlobalStats()
