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
            words_to_learn.add_word_pair(word_pair)
        return words_to_learn

    def words_to_review(self) -> WordList:
        """Returns a word list containing the words to review"""
        words_to_review = WordList(self.word_list_name, self._language_of_list)
        query = ("SELECT foreign_word, translated_word, when_review FROM " 
                 + Database.table_name + " WHERE is_known = 1 AND "
                 + "word_list_name = \'" + self.word_list_name + "\'") 
        result = self.db.result_from_query(query)
        print(result)
        for element in result:
            when_review = datetime.strptime(entry[3], "%d/%m/%Y %H:%M:%S")
            if now > when_review_obj:
                pass
        return words_to_review

    def _language_of_list(self):
        """Gets the language of the word list"""
        pass



if __name__ == "__main__":
    
    word_list = "Harry Potter und der Stein"

    word_selector = WordSelector(word_list)

    out_list = word_selector.words_to_review()
