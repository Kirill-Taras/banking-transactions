import json
from pathlib import Path

import pandas as pd

from src.views import get_file_xls


def increased_cashback(data_path: Path, year_: int, month_: int) -> str:
    operations = get_file_xls(data_path)

    if operations is None:
        return json.dumps({}, ensure_ascii=False, indent=2)

    start_cashback = f"{year_}-{month_}-01"
    start_cashback_dt = pd.to_datetime(start_cashback)
    operations["Дата операции"] = pd.to_datetime(operations["Дата операции"], dayfirst=True)

    interval_time = operations[
        start_cashback_dt.month == pd.to_datetime(operations["Дата операции"], dayfirst=True).dt.month
    ]
    interval_datetime = interval_time[start_cashback_dt.year == interval_time["Дата операции"].dt.year]

    dict_category = dict()
    list_category = list(interval_datetime["Категория"].unique())

    for category in list_category:
        if isinstance(category, str):
            sum_category = round(
                abs(
                    operations.loc[
                        (operations["Категория"] == category) & (operations["Сумма операции"] <= 0), "Сумма операции"
                    ].sum()
                ),
                2,
            )
            dict_category[category] = sum_category

    return json.dumps(dict_category, ensure_ascii=False, indent=2)
