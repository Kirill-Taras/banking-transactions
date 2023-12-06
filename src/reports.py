from datetime import datetime
from functools import wraps
from typing import Optional, Callable, Any

import pandas as pd

from src.config import FILE_OPERATIONS, FILE_REPORTS
from src.views import get_file_xls


operations = get_file_xls(FILE_OPERATIONS)


def printing_report(file_path=FILE_REPORTS) -> Callable:
    def wrapped(function: Callable) -> Callable:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                result = function(*args, **kwargs)
            except Exception:
                result = None
            result.to_excel(file_path, index=False)
            return result

        return inner

    return wrapped


@printing_report()
def spending_by_category(transactions: pd.DataFrame, category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция возвращает траты по заданной категории
    за последние 3 месяца (от переданной даты).
    :param transactions: датафрейм с транзакциями
    :param category: название категории
    :param date: опциональная дата
    :return: датафрейм c тратами по заданной категории
    """

    if date is None:
        date_f = datetime.now()
    else:
        date_f = pd.to_datetime(date)
    date_s = date_f.replace(month=date_f.month - 3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    interval_time = transactions[date_f >= transactions["Дата операции"]]
    interval_datetime = interval_time[date_s <= interval_time["Дата операции"]]
    by_category = interval_datetime[interval_datetime["Категория"] == category]
    return by_category
