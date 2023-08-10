"""__main__.py"""

import os

from pathlib import Path


def run():
    MAIN_PATH = str(Path(__file__).parents[0] / "src" / "gui" / "main_window.py")
    os.system(f"python {MAIN_PATH}")


if __name__ == "__main__":
    run()
