"""
file_reader.py
"""

from src.core.row import Row
from src.database.row_dao import RowDAO


class FileReader:
    """
    Responsible for reading and writing data containing vocabulary from a text
    file into the database.
    """
    def __init__(self, file_path):
        """Initializes a FileReader instance"""
        self.file_path = file_path

    def insert_into_db(self, rows, language, word_list_name):
        """Inserts the words from the file into the database"""
        pass

    def is_input_file_valid(self):
        """
        Checks whether the input file consists of two columns separated by a
        tab and that it is non-empty.
        """
        pass

    def _export_rows_from_file(self):
        """Converts the data in the file into a list of Rows"""
        pass
        # return rows


if __name__ == "__main__":
    print("file_reader.py")