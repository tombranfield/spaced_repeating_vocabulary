"""
list_dao.py
"""

from src.database.database import Database


class WordListDAO:
    """
    Acts as an interface to the database for getting data about a
    given word list.
    """
    def __init__(self, db_path=Database.path):
        """Initializes the word list data access object"""
        self.db = Database(db_path)

    def word_list_names(self):
        """Returns the names of all the word lists in the database"""
        query = "SELECT DISTINCT word_list_name FROM " + Database.table_name
        result = self.db.result_from_query(query)
        names = [entry[0] for entry in result]
        return names

    def language(word_list_name):
        """Returns the language of the given word list"""
        query = ("SELECT DISTINCT language FROM " + Database.table_name
                + " WHERE list_name = \'" + word_list_name + "\'" 
        result = self.db.result_from_query(query)
        return result[0][0]

    def num_words(word_list_name: str):
        pass

    def num_known_words(word_list_name: str):
        pass

    def num_unknown_words(word_list_name: str):
        pass


if __name__ == "__main__":

    my_list_dao = WordListDAO()
