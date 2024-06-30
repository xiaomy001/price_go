# -*- coding: utf-8 -*-

from daily_price import DailyPrice
from history_prices import HistoryPrices
import csv

class DataReader:

    def __init__(self) -> None:
        pass

    def make_history_prices(self, file_path) -> HistoryPrices:
        history_prices = HistoryPrices()
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                daily_price = DailyPrice(row[0], row[1], row[2], row[3], row[4])
                history_prices.add(daily_price)
        return history_prices

if __name__ == '__main__':
    data_reader = DataReader()
    history_prices = data_reader.make_history_prices('E:\\my_projects\\price_go\\data\\TQQQ_test.csv')
    print(history_prices)

