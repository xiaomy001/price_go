# -*- coding: utf-8 -*-

from datetime import date

class DailyPrice:

    def __init__(self, p_date, p_open, p_high, p_low, p_close) -> None:
        self.p_date = date.fromisoformat(p_date.replace('/', '-'))
        self.p_open = int(float(p_open) * 1000000)
        self.p_high = int(float(p_high) * 1000000)
        self.p_low = int(float(p_low) * 1000000)
        self.p_close = int(float(p_close) * 1000000)

    def get_avg_price(self) -> int:
        return int((self.p_open + self.p_low + self.p_close + self.p_high) / 4)
    
    def get_buy_price(self, trigger_price) -> int:
        # return min(int((self.p_close + self.p_high + trigger_price) / 3), self.p_high)
        # return min(trigger_price + min(max(int((self.p_high - trigger_price) / 2), 20000), int(self.p_high - trigger_price), 40000), self.p_high)
        return min(trigger_price + 50000, self.p_high + 10000)
    
    def get_sell_price(self, trigger_price) -> int:
        # return max(int((self.p_close + self.p_low + trigger_price) / 3), self.p_low)
        # return max(trigger_price - min(max(int((trigger_price - self.p_low) / 2), 20000), int(trigger_price - self.p_low), 40000), self.p_low)
        return max(trigger_price - 50000, self.p_low - 10000)

