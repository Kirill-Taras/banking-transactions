from datetime import datetime

import pytest

from src.utils import times_of_day


@pytest.mark.parametrize("time_real, expected", [("2023-12-04 21:49:08.466629", "Добрый вечер"),
                                                 ("2023-12-04 10:49:08.466629", "Доброе утро"),
                                                 ("2023-12-04 02:49:08.466629", "Доброй ночи"),
                                                 ("2023-12-04 15:49:08.466629", "Добрый день")])
def test_times_of_day(time_real, expected):
    time_now = datetime.strptime(time_real, "%Y-%m-%d %H:%M:%S.%f")
    assert times_of_day(time_now) == expected
