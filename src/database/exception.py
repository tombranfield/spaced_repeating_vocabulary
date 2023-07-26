"""duplicate_exception.py"""


class DuplicateEntryException(Exception):
    """Raised when inserting entry which already exists"""
    pass


class EmptyWordListException(Exception):
    """Raised when trying to use an empty word list"""
    pass
