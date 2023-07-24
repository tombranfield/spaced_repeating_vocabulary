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
    def __init__(self, file_path: str):
        """Initializes a FileReader instance"""
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        # Do some validation of this in case bad input?
        self._file_path = file_path

    def insert_into_database(self, language: str, word_list_name: str):
        """Inserts the words from the file into the database"""
        row_dao = RowDAO()
        rows = self._export_rows_from_file(language, word_list_name)
        row_dao.insert_rows(rows)

    def is_input_file_valid(self):
        """
        Checks whether the input file consists of two columns separated by a
        tab and that it is non-empty.
        """
        pass

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


if __name__ == "__main__":

    test_file_path = "../../TODO/short.txt"

    file_reader = FileReader(test_file_path)

    file_reader.insert_into_database("german", "harry potter")

    print("'file_reader.py' done")

