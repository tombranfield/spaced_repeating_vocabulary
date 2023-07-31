"""settings.py"""


from pathlib import Path


class Settings:
    """Responsible for the settings of the program"""
    PATH = str(Path(__file__).parents[2] / "data" / "settings.ini")

    DEFAULTS = {
        "is_case_sensitive": True,
        "is_automatic_return": True,
        "max_learn_words": 5,
        "max_review_words": 25,
    }

    def __init__(self, settings_path=PATH):
        self._path = settings_path
        self._is_case_sensitive = Settings.DEFAULTS["is_case_sensitive"]
        self._is_automatic_return = Settings.DEFAULTS["is_automatic_return"]
        self._max_learn_words = Settings.DEFAULTS["max_learn_words"]
        self._max_review_words = Settings.DEFAULTS["max_review_words"]

    @property
    def is_case_sensitive(self):
        return self._is_case_sensitive

    @is_case_sensitive.setter
    def is_case_sensitive(self, answer: bool):
        self._is_case_sensitive = str(answer)
        self._write_to_file()

    @property
    def is_automatic_return(self):
        return self._is_automatic_return

    @is_automatic_return.setter
    def is_automatic_return(self, answer: bool):
        self._is_automatic_return = str(answer)
        self._write_to_file()

    @property
    def max_learn_words(self):
        return self._max_learn_words

    @max_learn_words.setter
    def max_learn_words(self, number: int):
        self._max_learn_words = str(number)
        self._write_to_file()

    @property
    def max_review_words(self):
        return self._max_review_words

    @max_review_words.setter
    def max_review_words(self, number: int):
        self._max_review_words = str(number)
        self._write_to_file()

    def set_defaults(self):
        self._is_case_sensitive = self.DEFAULTS["is_case_sensitive"]
        self._is_automatic_return = self.DEFAULTS["is_automatic_return"]
        self._max_learn_words = self.DEFAULTS["max_learn_words"]
        self._max_review_words = self.DEFAULTS["max_review_words"]
        self._write_to_file()

    def _write_to_file(self):
        with open(self._path, "w") as w_obj:
            w_obj.write("is_case_sensitive=" + str(self.is_case_sensitive) + "\n")
            w_obj.write("is_automatic_return=" + str(self.is_automatic_return) + "\n")
            w_obj.write("max_learn_words=" + str(self.max_learn_words) + "\n")
            w_obj.write("max_review_words=" + str(self.max_review_words) + "\n")




if __name__ == "__main__":
    settings = Settings("here_settings.txt")
    settings.is_case_sensitive = False
    settings.max_learn_words = 10
    settings.set_defaults()
