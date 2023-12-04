from datetime import datetime


def times_of_day(current_datetime=datetime.now()) -> str:
    """
    Функция возвращает приветственный текст,
    в зависимости от времени суток.
    :return: Приветствие.
    """
    if 6 <= current_datetime.hour < 12:
        welcome_text = "Доброе утро"
    elif 12 <= current_datetime.hour < 18:
        welcome_text = "Добрый день"
    elif 18 <= current_datetime.hour < 24:
        welcome_text = "Добрый вечер"
    elif 0 <= current_datetime.hour < 6:
        welcome_text = "Доброй ночи"
    else:
        welcome_text = "Некорректное время"
    return welcome_text
