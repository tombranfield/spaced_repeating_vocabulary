"""
Holds the constants for the application
"""


class Constants:
    """Holds the constants for the application"""
    def __init__(self):
        self._db_path = "wordlists.db"

    @property
    db_path(self) -> str:
        """Returns the path to the database"""
        return self._db_path
