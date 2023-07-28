"""word_selector.py"""


from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.database.database import Database


class WordSelector:
    """
    Responsible for choosing words to learn or review from the database.
    """
    def __init__(self, word_list_name, db_path=Database.path):
        self.word_list_name = word_list_name
        self.db = Database(db_path)


    def words_to_learn(self) -> WordList:
        """Returns a word list containing the words to learn"""
        words_to_learn = WordList(self.word_list_name, self._language_of_list)
        query = ("SELECT foreign_word, translated_word FROM " 
                 + Database.table_name + " WHERE is_known = 0 AND "
                 + "word_list_name = \'" + self.word_list_name + "\'") 
        result = self.db.result_from_query(query)
        for pair in result:
            word_pair = WordPair(*pair)
            word_to_learn.add_word_pair(word_pair)
        return words_to_learn


    def words_to_review(self) -> WordList:
        """Returns a word list containing the words to review"""
        # db.get_words_to_review(self.list_name)
        pass


    def _language_of_list(self):
        """Gets the language of the word list"""
        pass


    def _reviewable_words(self):
        pass


if __name__ == "__main__":
    
    word_list = "Harry Potter und der Stein"

    word_selector = WordSelector(word_list)

    word_selector.words_to_learn()
