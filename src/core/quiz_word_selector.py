"""quiz_word_selector.py"""


from datetime import datetime

from src.core.quiz_word import QuizWord
from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.database.database import Database


class QuizWordSelector:
    """
    Responsible for choosing words to learn or review from the database.
    """
    def __init__(self, word_list_name, db_path=Database.path):
        self.word_list_name = word_list_name
        self.db = Database(db_path)

    def words_to_learn(self):
        """Returns a word list containing the words to learn"""
#        words_to_learn = WordList(self.word_list_name, self._language_of_list)
        words_to_learn = ()
        query = (
            "SELECT rowid, foreign_word, translated_word FROM " 
            + Database.table_name + " WHERE is_known = 0 AND "
            + "word_list_name = \'" + self.word_list_name + "\'"
        ) 
        result = self.db.result_from_query(query)
        for entry in result:
            id = entry[0]
            word_pair = WordPair(entry[1], entry[2])
            quiz_word = QuizWord(id, word_pair)
            words_to_learn += (quiz_word,)
#        for pair in result:
#            word_pair = WordPair(*pair)
#            words_to_learn.add_word_pair(word_pair)
#        return words_to_learn
        return words_to_learn

    def words_to_review(self):
        """Returns a word list containing the words to review"""
#        words_to_review = WordList(self.word_list_name, self._language_of_list)
        words_to_review =  ()
        query = (
            "SELECT rowid, foreign_word, translated_word, when_review FROM " 
            + Database.table_name + " WHERE is_known = 1 AND "
            + "word_list_name = \'" + self.word_list_name + "\'"
        ) 
        result = self.db.result_from_query(query)
        reviewable_words = {}
        for entry in result:
            when_review = datetime.strptime(entry[3], "%d/%m/%Y %H:%M:%S")
            if datetime.now() > when_review:
                id = entry[0]
                word_pair = WordPair(entry[1], entry[2])
                quiz_word = QuizWord(id, word_pair, "review")
                # words_to_review += (quiz_word,)
                reviewable_words[quiz_word] = when_review
        reviewable_words = sorted(reviewable_words.items(), key = lambda x: x[1])
        for entry in reviewable_words:
            words_to_review += (entry[0],)
#                word_pair = WordPair(entry[0], entry[1])
#                words_to_review.add_word_pair(word_pair)
        return words_to_review

    def all_course_words(self):
        """Returns all the words of the course in a format for the quiz"""
        all_course_words = ()
        query = (
            "SELECT rowid, foreign_word, translated_word FROM "
            + Database.table_name + " WHERE word_list_name = \'"
            + self.word_list_name + "\'"
        )
        result = self.db.result_from_query(query)
        for entry in result:
            id = entry[0]
            word_pair = WordPair(entry[1], entry[2])
            quiz_word = QuizWord(id, word_pair)
            all_course_words += (quiz_word,)
        return all_course_words



if __name__ == "__main__":
    
    word_list = "Harry Potter und der Stein"

    word_selector = WordSelector(word_list)

    out_list = word_selector.words_to_review()
