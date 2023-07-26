"""
file_reader.py
"""

# from src.core.row import Row
from src.core.word_list import WordList
from src.core.word_pair import WordPair
from src.database.database import Database
# from src.database.row_dao import RowDAO
from src.database.word_list_dao import WordListDAO


class FileReader:
    """
    Responsible for reading and writing data containing vocabulary from a text
    file into the database.
    """
    def __init__(self, file_path: str, db_path=Database.path):
        """Initializes a FileReader instance"""
        self._file_path = file_path
        self._db_path = db_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        # Do some validation of this in case bad input?
        self._file_path = file_path

    """
    def insert_into_database(self, language: str, word_list_name: str):
        # Inserts the words from the file into the database
        row_dao = RowDAO(self._db_path)
        rows = self._export_rows_from_file(language, word_list_name)
        row_dao.insert_rows(rows)
    """

    def insert_into_database(self, word_list: WordList):
        """Inserts the word from the file into the database"""
        word_pairs = self._export_word_pairs_from_file()


    def _export_word_pairs_from_file(self):
        """Extracts the pairs of foreign words and their translations"""
        word_pairs = ()
        with open(self.file_path, "r", encoding="utf-8") as file_obj:
            for line in file_obj:
                line = line.strip().split("\t")
                word_pair = WordPair(line[0].strip(), line[1])
                word_pairs += word_pair
        return word_pairs


    # Replace with word pairs -> making rows is unnecessary
    def _export_rows_from_file(self, language: str, word_list_name: str):
        """
        Converts the data in the file into a list of tuples containing
        pairs of foreign words with their respective translations.
        """
        rows = []
        with open(self.file_path, "r", encoding="utf-8") as file_obj:
            for line in file_obj:
                # Tab-delimited
                line = line.strip().split("\t")
                row = Row(line[0].strip(), line[1], language, word_list_name)
                rows.append(row)
        return rows


    def is_input_file_valid(self):
        """
        Checks whether the input file consists of two columns separated by a
        tab and that it is non-empty.
        """
        pass


if __name__ == "__main__":

    test_file_path = "../../TODO/short.txt"

    file_reader = FileReader(test_file_path)

    new_path = "hooray.txt"

    file_reader.file_path = new_path

    print(file_reader.file_path)

#    file_reader.insert_into_database("german", "harry potter")

    print("'file_reader.py' done")

