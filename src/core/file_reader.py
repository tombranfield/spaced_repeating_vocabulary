"""
file_reader.py
"""

from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.database.database import Database
from src.database.word_list_dao import WordListDAO


class FileReader:
    """
    Responsible for reading and writing data containing vocabulary from a text
    file into the database.
    """
    def __init__(self, file_path: str="", db_path=Database.path):
        """Initializes a FileReader instance"""
        self._file_path = file_path
        self._db_path = db_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        self._file_path = file_path

    def insert_into_database(self, word_list_name, language):
        """Inserts the word from the file into the database"""        
        word_pairs = self._export_word_pairs_from_file()
        word_list = WordList(word_list_name, language, word_pairs)
        word_list_dao = WordListDAO(self._db_path)
        word_list_dao.insert_word_list(word_list)

    def _export_word_pairs_from_file(self):
        """Extracts the pairs of foreign words and their translations"""
        word_pairs = ()
        try:
            file_obj = open(self._file_path, "r", encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError
        else:
            for line in file_obj:
                line = line.strip().split("|")
                try:
                    word_pair = WordPair(str(line[0].strip()), str(line[1]))
                except IndexError:
                    raise IndexError("Two tab-delimited columns required")
                else:
                    if len(line) > 2:
                        raise ValueError("Incorrect file format")
                    else:
                        word_pairs += (word_pair,)
            return word_pairs


    def is_input_file_valid(self):
        """
        Checks whether the input file consists of two columns separated by a
        tab and that it is non-empty.
        """
        try:
            word_pair_list = self._export_word_pairs_from_file()
        except:
            return False
        else:
            return True



if __name__ == "__main__":

    test_file_path = "../../TODO/short.txt"

    file_reader = FileReader(test_file_path)

    print(file_reader.file_path)    

    file_reader.insert_into_database("harry potterzzz", "german")

    print("'file_reader.py' done")

