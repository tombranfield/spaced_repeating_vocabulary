"""course.py"""


from dataclasses import dataclass


@dataclass
class Course:
    """
    A dataclass that represents a course
    """
    name: str = ""
    language: str = ""
