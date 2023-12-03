import json
from pathlib import Path

from src.utils import times_of_day
from src.views import get_currency_rate, get_dict_card, get_stocks_rate, get_top_transactions

FILE_OPERATIONS = Path.joinpath(Path(__file__).parent.parent, "data", "operations.xls")
FILE_USER_SETTINGS = Path.joinpath(Path(__file__).parent.parent, "user_settings.json")


def main() -> str:
    """
    Функция, которая выдает json-ответ с данными.
    :return: json-ответ.
    """
    user_date = input("Введите дату в формате YYYY-MM-DD: ")
    json_answer = dict()
    json_answer["greeting"] = times_of_day()
    json_answer["cards"] = get_dict_card(FILE_OPERATIONS, user_date)
    json_answer["top_transactions"] = get_top_transactions(FILE_OPERATIONS, user_date)
    json_answer["currency_rates"] = get_currency_rate(FILE_USER_SETTINGS)
    json_answer["stock_prices"] = get_stocks_rate(FILE_USER_SETTINGS)
    return json.dumps(json_answer, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(type(main()))
