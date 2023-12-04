import pytest

from src.config import FILE_OPERATIONS, FILE_USER_SETTINGS
from src.views import (get_currency_rate, get_dict_card, get_file_xls, get_stocks_rate, get_time_interval,
                       get_top_transactions)


def test_get_file_xls():
    assert get_file_xls(FILE_OPERATIONS).loc[0, "Номер карты"] == "*7197"
    assert get_file_xls("user_settings.json") == None


def test_get_time_interval():
    assert get_time_interval(FILE_OPERATIONS, "2018-10-10").shape == (49, 15)


@pytest.mark.parametrize(
    "file_, date_user, expected",
    [(FILE_OPERATIONS, "2018-10-10", {"last_digits": "7197", "total_spent": 12090.24, "cashback": 120.9})],
)
def test_get_dict_card(file_, date_user, expected):
    assert get_dict_card(file_, date_user)[0] == expected


@pytest.mark.parametrize(
    "file_, date_user, expected",
    [
        (
            FILE_OPERATIONS,
            "2018-10-10",
            {
                "date": "04.10.2018",
                "amount": 104586.0,
                "category": "Переводы",
                "description": "Вывод средств с брокерского счета",
            },
        )
    ],
)
def test_get_top_transaction(file_, date_user, expected):
    assert get_top_transactions(file_, date_user)[0] == expected


def test_get_currency_rate():
    assert get_currency_rate(FILE_USER_SETTINGS)[0]['currency'] == "USD"
    assert get_currency_rate(FILE_USER_SETTINGS)[1]['currency'] == "EUR"


def test_get_stocks_rate():
    assert get_stocks_rate(FILE_USER_SETTINGS)[0]['price'] == "AAPL"
