import json
import os
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Optional, Union

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()
api_currency = os.environ.get("API_KEY_CURRENCY")
api_stocks = os.environ.get("API_KEY_STOCKS")


def get_file_xls(file_path: Path) -> Optional[DataFrame]:
    """
    Функция, которая принимает на вход путь к файлу xls,
    и возвращает данные по каждой карте.
    :param file_path: путь к файлу
    :return: данные по карте в формате python
    """
    try:
        operations = pd.read_excel(file_path)
    except (FileNotFoundError, UnicodeDecodeError, ImportError):
        operations = None
    return operations


def get_time_interval(file_path: Path, user_date: str) -> Optional[DataFrame]:
    """
    Функция, которая принимает дату от пользователя
    и собирает данные с начала того месяца, который указал пользователь.
    :param file_path: путь к файлу с данными.
    :param user_date: дата пользователя.
    :return: данные с конкретный период времени.
    """

    operations = get_file_xls(file_path)

    if operations is None:
        return None

    actual_date = pd.to_datetime(user_date)
    start_date_str = f"{actual_date.year}-{actual_date.month}-01"
    start_date_dt = pd.to_datetime(start_date_str)
    operations["Дата операции"] = pd.to_datetime(operations["Дата операции"], dayfirst=True)
    interval_time = operations[actual_date >= operations["Дата операции"]]
    interval_datetime = interval_time[start_date_dt <= interval_time["Дата операции"]]
    return interval_datetime


def get_dict_card(file_path: Path, user_date: str) -> list[dict[str, Any]]:
    """
    Функция, которая собирает данные о картах,
    используемые в период времени указанном пользователем.
    :param file_path: путь к файлу с данными.
    :param user_date: дата указанная пользователем
    :return: список со словарями, где хранятся данные
    """
    operations = get_time_interval(file_path, user_date)
    list_info_card = list()
    if operations is not None:
        list_card = list(operations["Номер карты"].unique())
        for card in list_card:
            dict_card = dict()
            if isinstance(card, str):
                sum_card = round(
                    abs(
                        operations.loc[
                            (operations["Номер карты"] == card) & (operations["Сумма операции"] <= 0),
                            "Сумма операции",
                        ].sum()
                    ),
                    2,
                )
                cashback = round(sum_card / 100, 2)
                dict_card["last_digits"] = card[1:5]
                dict_card["total_spent"] = sum_card
                dict_card["cashback"] = cashback
                list_info_card.append(dict_card)
    return list_info_card


def get_top_transactions(file_path: Path, user_date: str) -> list[dict[str, Any]]:
    """
    Функция, которая собирает данные о самых крупных транзакциях,
    совершенные в период времени указанный пользователем.
    :param file_path: путь к файлу с данными.
    :param user_date: дата указанная пользователем
    :return: список со словарями, где хранятся данные
    """
    operations = get_time_interval(file_path, user_date)
    list_top_transactions = list()
    if operations is not None:
        sorted_by_operations = operations.sort_values("Сумма операции с округлением", ascending=False).head()
        for i, row in sorted_by_operations.iterrows():
            dict_transactions = dict()
            dict_transactions["date"] = row["Дата платежа"]
            dict_transactions["amount"] = row["Сумма операции"]
            dict_transactions["category"] = row["Категория"]
            dict_transactions["description"] = row["Описание"]
            list_top_transactions.append(dict_transactions)
    return list_top_transactions


def get_currency_rate(file_json: Path) -> list[dict[str, Union[str, float]]]:
    """
    Функция, которая забирает данные через API и передает
    необходимую информацию в словари по данным валютам.
    :param file_json: путь к файлу с настройками
    :return: список со словарями по курсу валют
    """
    try:
        with open(file_json, encoding="utf-8") as data:
            user_settings = json.load(data)
    except (FileNotFoundError, JSONDecodeError):
        user_settings = list()
    base_user = user_settings.get("user_currencies", [])
    list_currency = list()
    for base in base_user:
        currency_rates = dict()
        url = "https://api.apilayer.com/exchangerates_data/latest"
        try:
            response = requests.get(url, params={"base": base, "apikey": api_currency})
            response_json = response.json()
            currency_rates["currency"] = response_json["base"]
            currency_rates["rate"] = response_json["rates"].get("RUB", 0.0)
            list_currency.append(currency_rates)
        except Exception:
            list_currency = list()
    return list_currency


def get_stocks_rate(file_json: Path) -> list[dict[str, Union[str, float]]]:
    """
    Функция, которая забирает данные через API и передает
    необходимую информацию в словари по данным акциям.
    :param file_json: путь к файлу с настройками
    :return: список со словарями по акциям
    """
    try:
        with open(file_json, encoding="utf-8") as data:
            user_settings = json.load(data)
    except (FileNotFoundError, JSONDecodeError):
        user_settings = list()
    stocks_user = user_settings.get("user_stocks", [])
    list_stocks = list()
    for stocks in stocks_user:
        user_stocks = dict()
        url = "http://api.marketstack.com/v1/intraday/latest"
        try:
            response = requests.get(url, params={"access_key": api_stocks, "symbols": stocks})
            response_json = response.json()
            user_stocks["stock"] = response_json["data"][0].get("close", 0.0)
            user_stocks["price"] = response_json["data"][0].get("symbol", "")
            list_stocks.append(user_stocks)
        except Exception:
            list_stocks = list()
    return list_stocks
