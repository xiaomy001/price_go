# -*- coding: utf-8 -*-

from datetime import date

class TradingDays:

    def __init__(self) -> None:
        self.date_list = list()
        self.date_map = map()

    def add_date(self, c_date: date) -> None:
        self.date_list.append(c_date)
        self.date_map[c_date.isoformat()] = len(self.date_list) - 1

    def check_next_day_in_same_week(self, c_date: date) -> bool:
        pass

