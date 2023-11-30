from pathlib import Path

import pandas as pd
from pandas import DataFrame


FILE_OPERATIONS = Path.joinpath(Path(__file__).parent.parent, "data", "operations.xls")


def get_file_xls(file_path: Path) -> None | DataFrame:
    """
    Функция, которая принимает на вход путь к файлу xls,
    и возвращает данные для чтения в python.
    :param file_path: путь к файлу
    :return: данные в формате python
    """
    try:
        operations = pd.read_excel(file_path)
    except (FileNotFoundError, UnicodeDecodeError, ImportError):
        operations = None
    return operations


# print(get_file_xls(FILE_OPERATIONS))
