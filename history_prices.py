# -*- coding: utf-8 -*-

from daily_price import DailyPrice

class HistoryPrices:

    def __init__(self) -> None:
        self.daily_price_list: list[DailyPrice] = list()
        self.date_index: dict[str:int] = dict()

    def add(self, daily_price: DailyPrice) -> None:
        self.daily_price_list.append(daily_price)
        self.date_index[daily_price.p_date.isoformat()] = len(self.daily_price_list) - 1
