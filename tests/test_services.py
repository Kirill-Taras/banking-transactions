import json

import pytest


from src.config import FILE_OPERATIONS
from src.services import increased_cashback


@pytest.fixture()
def dict_category():
    dict_fix = {
        "Супермаркеты": 378115.51,
        "Ж/д билеты": 128517.85,
        "Транспорт": 91826.89,
        "Фастфуд": 173295.7,
        "Образование": 651056.61,
        "Различные товары": 143324.16,
        "Книги": 4634.0,
        "Сервис": 33807.53,
        "Связь": 65940.39,
        "Услуги банка": 14477.09,
        "Аптеки": 67895.09,
        "Наличные": 632407.7,
        "Переводы": 4942002.09,
        "Цветы": 10953.0,
        "Рестораны": 63152.75,
        "Другое": 245604.32,
        "Мобильная связь": 4470.0,
        "Дом и ремонт": 186375.1,
        "Одежда и обувь": 31566.52,
    }
    return json.dumps(dict_fix, ensure_ascii=False, indent=2)


def test_increased_cashback(dict_category):
    assert increased_cashback(FILE_OPERATIONS, 2018, 11) == dict_category
