import os

import pandas as pd

from src.config import TEST_FILE_REPORTS, FILE_OPERATIONS
from src.reports import printing_report


def test_printing_report():
    if TEST_FILE_REPORTS.exists():
        os.remove(TEST_FILE_REPORTS)

    @printing_report(file_path=TEST_FILE_REPORTS)
    def foo(filepath):
        try:
            operations = pd.read_excel(filepath)
        except (FileNotFoundError, UnicodeDecodeError, ImportError):
            operations = None
        return operations.loc[0:1, "Категория"]

    foo(FILE_OPERATIONS)
    test_file = pd.read_excel(TEST_FILE_REPORTS)

    assert test_file == foo(FILE_OPERATIONS)
