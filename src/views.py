import os
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
import pandas as pd
import requests
from pandas import DataFrame


FILE_OPERATIONS = Path.joinpath(Path(__file__).parent.parent, "data", "operations.xls")
load_dotenv()
api_currency = os.environ.get("API_KEY_CURRENCY")
api_stocks = os.environ.get("API_KEY_STOCKS")


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


def get_currency_rate(base: str) -> dict | None:
    """
    Функция, которая считывает данные.
    :param base:
    :return:
    """
    url = "https://api.apilayer.com/exchangerates_data/latest"
    try:
        response = requests.get(url,  params={"base": base, "apikey": api_currency})
        response_json = response.json()
    except Exception:
        response_json = None
    return response_json


def get_stocks_rate(stocks: str) -> dict:
    url = "http://api.marketstack.com/v1/intraday/latest"
    try:
        response = requests.get(url, params={"access_key": api_stocks, "symbols": stocks})
        response_json = response.json()
    except Exception:
        response_json = None
    return response_json


# pprint(get_stocks_rate("TSLA"))
pprint(get_currency_rate("USD"))
