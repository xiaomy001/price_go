# -*- coding: utf-8 -*-

from tool import Tool
from ex_iterator import ExIterator
from daily_price import DailyPrice
from enum import Enum, auto
import csv
from datetime import date


def calculate_decline(highest_daily_price: DailyPrice, current_daily_price: DailyPrice) -> float:
    diff = highest_daily_price.p_high - current_daily_price.p_low
    return round(diff * 100 / highest_daily_price.p_high, 2)


trigger_line = 55
factor = 20
def calculate_rebalance_stage(decline: float) -> int:
    if decline < trigger_line:
        return 0
    else:
        return int((decline - trigger_line) / factor) + 1


def get_trigger_price(stage, high_price) -> int:
    if stage == 1:
        percent = (100 - trigger_line) / 100
    else:
        percent = (100 - trigger_line - (stage - 1) * factor) / 100
    return int(high_price * percent)


class RebalanceCaseEnum(Enum):
    CASE_0 = (0.5, 0.5)
    CASE_1 = (0.53, 0.47)
    CASE_2 = (0.57, 0.43)
    CASE_3 = (0.62, 0.38)
    CASE_4 = (0.68, 0.32)
    CASE_5 = (0.75, 0.25)
    CASE_6 = (0.82, 0.18)
    CASE_7 = (0.88, 0.12)
    CASE_8 = (0.93, 0.07)
    CASE_9 = (0.97, 0.03)
    CASE_10 = (1, 0)


class SmileSignEnum(Enum):
    LEFT = auto()
    RIGHT = auto()
    RECOVERY_AND_START_NEW = auto()


class Smile:

    def __init__(self, data_source: ExIterator) -> None:
        self.data_source = data_source
        self.is_smiling: bool = False
        self.highest: DailyPrice = None
        self.lowest: DailyPrice = None
        self.max_decline = None
        self.current: DailyPrice = None
        self.current_decline = None

    def forward(self) -> SmileSignEnum:
        self.current = self.data_source.current()
        if self.highest is None or (not self.is_smiling and self.current.p_high > self.highest.p_high):
            self._reset()
            return SmileSignEnum.LEFT
        
        if self.is_smiling and self.current.p_low >= self.highest.p_high:
            self._reset()
            return SmileSignEnum.RECOVERY_AND_START_NEW

        decline = calculate_decline(self.highest, self.current)
        self.current_decline = decline

        if self.current.p_low < self.lowest.p_low:
            self.lowest = self.current
            self.max_decline = decline
            return SmileSignEnum.LEFT
        else:
            return SmileSignEnum.RIGHT
        
    def set_smiling(self):
        self.is_smiling = True
    
    def _reset(self):
        decline = calculate_decline(self.current, self.current)
        self.is_smiling = False
        self.highest = self.current
        self.lowest = self.current
        self.max_decline = decline
        self.current_decline = decline


multiple = 1000000
report_headers = [
    'date',
    'spy decline',
    'qqq decline',
    'tqqq decline',
    'prev work day',
    'decline stage',
    'rebalance stage',
    'price range',
    'trade price',
    'trigger price',
    'before stock quantity',
    'before stock amount',
    'before cash amount',
    'after stock quantity',
    'after stock amount',
    'after cash amount',
    'total amount',
    'left amount',
]


class RebalanceTool(Tool):

    def __init__(self, spy_data_source: ExIterator, qqq_data_source: ExIterator, output_path, data_source: ExIterator, stock_amount: int, cash_amount: int) -> None:
        super().__init__()
        self.spy_data_source = spy_data_source
        self.qqq_data_source = qqq_data_source
        self.output_path = output_path
        self.data_source = data_source
        self.startup_stock_amount = stock_amount * multiple
        self.startup_stock_count = 0
        self.stock_count = 0
        self.cash_amount = cash_amount * multiple
        self.spy_smile: Smile = Smile(spy_data_source)
        self.qqq_smile: Smile = Smile(qqq_data_source)
        self.tqqq_smile: Smile = Smile(data_source)
        self.decline_stage = 0
        self.rebalance_stage = 0
        self.report_list: list[list] = [report_headers]
        self.current_daily_price: DailyPrice = None
        self.intervals: dict[int, date] = dict()
        self.rebalance_price = 0
        self.prev_work_day: date = None

    def get_data_sources(self) -> set[ExIterator]:
        return {self.spy_data_source, self.qqq_data_source, self.data_source}
    
    def execute(self):
        self.current_daily_price = self.data_source.current()
        self._init_stock_and_cash()
        need_rebalance = self._check_rebalance()
        if need_rebalance and not self._is_cooling():
            self._rebalance()
        self.prev_work_day = self.current_daily_price.p_date

    def _init_stock_and_cash(self):
        if self.stock_count == 0:
            price = self.current_daily_price.get_avg_price()
            quantity = int(self.startup_stock_amount / price)
            cost = quantity * price

            self.stock_count += quantity
            self.startup_stock_count = self.stock_count
            self.cash_amount += self.startup_stock_amount - cost

            current_stock_amount = round(cost / multiple, 2)
            current_cash_amount = round(self.cash_amount / multiple, 2)
            total_amount = round(current_stock_amount + current_cash_amount)
            report = [
                self.current_daily_price.p_date.isoformat(),
                '',
                '',
                '',
                '',
                self.decline_stage,
                self.rebalance_stage,
                f"{round(self.current_daily_price.p_low / multiple , 4)} - {round(self.current_daily_price.p_high / multiple , 4)}",
                round(price / multiple , 4),
                '',
                '',
                '',
                '',
                self.stock_count,
                current_stock_amount,
                current_cash_amount,
                total_amount,
                round(current_stock_amount),
            ]
            self.report_list.append(report)

    def _check_rebalance(self) -> bool:
        spy_sign = self.spy_smile.forward()
        qqq_sign = self.qqq_smile.forward()
        tqqq_sign = self.tqqq_smile.forward()
        # if not qqq_sign is SmileSignEnum.RIGHT:
        #     self._reset_rebalance_stage_when_restart(qqq_sign)
        #     self._set_smiling(self.spy_smile)
        #     self._set_smiling(self.qqq_smile)
        #     return self._trigger_rebalance(spy_sign)
        # return False

        self._reset_rebalance_stage_when_restart(tqqq_sign)
        self._set_smiling(self.spy_smile)
        self._set_smiling(self.qqq_smile)
        self._set_smiling(self.tqqq_smile)
        stage = calculate_rebalance_stage(self.tqqq_smile.current_decline)
        if stage > self.decline_stage:
            self.rebalance_stage = self.decline_stage + 1
            self.decline_stage = stage
            if self.rebalance_stage == 1:
                trigger_price = self._convert_rebalance_stage_to_trigger_price()
                self.rebalance_price = self.current_daily_price.get_sell_price(trigger_price)
            return True
        if self.rebalance_stage > 0 and self.current_daily_price.p_high > self.rebalance_price:
            self.rebalance_stage = 0
            self.decline_stage = 0
            return True
        # if self.rebalance_stage > 0 and self.current_daily_price.p_low > self.rebalance_price:
        #     self.rebalance_stage = 0
        #     return True
        return False

    def _reset_rebalance_stage_when_restart(self, sign):
        if sign is SmileSignEnum.RECOVERY_AND_START_NEW:
            self.rebalance_stage = 0
            self.decline_stage = 0

    def _set_smiling(self, smile: Smile):
        if not smile.is_smiling and smile.current_decline > 5:
            smile.set_smiling()

    def _convert_rebalance_stage_to_trigger_price(self) -> int:
        return get_trigger_price(self.rebalance_stage, self.tqqq_smile.highest.p_high)

    def _trigger_rebalance(self, spy_sign: SmileSignEnum) -> bool:
        stage = calculate_rebalance_stage(self.qqq_smile.current_decline)
        if stage > self.rebalance_stage:
            self.rebalance_stage = stage
            return True
        return False

        # if self.rebalance_stage == 0:
        #     if self._trigger_first_rebalance(spy_sign):
        #         self.rebalance_stage = calculate_rebalance_stage(self.qqq_smile.current_decline)
        #         return True
        # else:
        #     stage = calculate_rebalance_stage(self.qqq_smile.current_decline)
        #     if stage > self.rebalance_stage:
        #         self.rebalance_stage = stage
        #         return True
        # return False

    def _trigger_first_rebalance(self, spy_sign) -> bool:
        if not spy_sign is SmileSignEnum.RIGHT and self.spy_smile.current_decline > 5 and self.qqq_smile.current_decline > 5:
            return True
        elif self.qqq_smile.current_decline > 5:
            return True
        
    def _is_cooling(self) -> bool:
        return False
        # if self.rebalance_stage > 1:
        #     return False
        # else:
        #     return True
        
        # if self.rebalance_stage > 0 and self.rebalance_stage in self.intervals:
        #     prev_rebalance_date = self.intervals.get(self.rebalance_stage)
        #     delta = self.current_daily_price.p_date - prev_rebalance_date
        #     if delta.days > 365:
        #         return False
        #     else:
        #         return True
        # return False
        
    def _rebalance(self):
        rebalanced_cash_amount = self._calculate_rebalanced_cash_amount()
        buy_amount = self.cash_amount - rebalanced_cash_amount
        if buy_amount > 0:
            is_buy = True
        else:
            buy_amount = buy_amount * -1
            is_buy = False
        self._adjust_position(buy_amount, is_buy)

    def _calculate_rebalanced_cash_amount(self) -> int:
        (stock_amount_percent, cash_amount_percent) = self._get_rebalance_percent()
        trigger_price = self._convert_rebalance_stage_to_trigger_price()
        price = self.current_daily_price.get_buy_price(trigger_price)
        total_amount = self.cash_amount + self.stock_count * price
        return round(total_amount * cash_amount_percent)
        
    def _get_rebalance_percent(self) -> tuple[float, float]:
        # diff = min((self.rebalance_stage - 1) * 5, 50)
        # return ((50 + diff) / 100, (50 - diff) / 100)
        # if self.rebalance_stage == 1:
        #     return (0.5, 0.5)
        # elif self.rebalance_stage == 2:
        #     return (0.6, 0.4)
        # elif self.rebalance_stage == 3:
        #     return (0.7, 0.3)
        # elif self.rebalance_stage == 4:
        #     return (0.8, 0.2)
        # elif self.rebalance_stage == 5:
        #     return (0.9, 0.1)
        # else:
        #     return (1, 0)
        
        if self.rebalance_stage < 1:
            return (1, 0)
        else:
            return (0.5, 0.5)
    
    def _adjust_position(self, amount: int, is_buy: bool):
        if self.rebalance_stage == 1:
            report = [
                self.tqqq_smile.highest.p_date.isoformat(),
                '',
                '',
                '',
                '',
                'highest',
                'highest',
                f"{round(self.tqqq_smile.highest.p_low / multiple , 4)} - {round(self.tqqq_smile.highest.p_high / multiple , 4)}",
                '',
                '',
                '',
                '',
                '',
                self.stock_count,
                round(self.stock_count * self.tqqq_smile.highest.p_close / multiple, 2),
                round(self.cash_amount / multiple, 2),
                round((self.stock_count * self.tqqq_smile.highest.p_close + self.cash_amount) / multiple),
                round(self.startup_stock_count * self.tqqq_smile.highest.p_close / multiple),
            ]
            self.report_list.append(report)

        trigger_price = self.rebalance_price if self.rebalance_stage == 0 else self._convert_rebalance_stage_to_trigger_price()
        price = self.current_daily_price.get_buy_price(trigger_price) if self.rebalance_stage == 0 else self.current_daily_price.get_sell_price(trigger_price)
        report = [
            self.current_daily_price.p_date.isoformat(),
            self.spy_smile.current_decline,
            self.qqq_smile.current_decline,
            self.tqqq_smile.current_decline,
            self.prev_work_day.isoformat(),
            self.decline_stage,
            self.rebalance_stage,
            f"{round(self.current_daily_price.p_low / multiple , 4)} - {round(self.current_daily_price.p_high / multiple , 4)}",
            round(price / multiple , 4),
            round(trigger_price / multiple , 4),
            self.stock_count,
            round(self.stock_count * price / multiple, 2),
            round(self.cash_amount / multiple, 2),
        ]

        quantity = int(amount / price)
        cost = quantity * price
        if is_buy:
            self.stock_count += quantity
            self.cash_amount -= cost
        else:
            self.stock_count -= quantity
            self.cash_amount += cost

        # self.intervals[self.rebalance_stage] = self.current_daily_price.p_date
        if self.rebalance_stage == 0:
            self.rebalance_price = 0

        report.append(self.stock_count)
        current_stock_amount = round(self.stock_count * price / multiple, 2)
        current_cash_amount = round(self.cash_amount / multiple, 2)
        total_amount = round(current_stock_amount + current_cash_amount)
        left_amount = round(self.startup_stock_count * price / multiple)
        report.append(current_stock_amount)
        report.append(current_cash_amount)
        report.append(total_amount)
        report.append(left_amount)
        self.report_list.append(report)

    def report(self) -> list[str]:
        current_stock_amount = round(self.stock_count * self.current_daily_price.p_close / multiple)
        current_cash_amount = round(self.cash_amount / multiple, 2)
        total_amount = round(current_stock_amount + current_cash_amount)
        left_amount = round(self.startup_stock_count * self.current_daily_price.p_close / multiple)
        report = [
            self.current_daily_price.p_date.isoformat(),
            '',
            '',
            '',
            self.prev_work_day.isoformat(),
            self.tqqq_smile.current_decline,
            self.tqqq_smile.current_decline,
            f"{round(self.current_daily_price.p_low / multiple , 4)} - {round(self.current_daily_price.p_high / multiple , 4)}",
            round(self.current_daily_price.get_avg_price() / multiple, 4),
            '',
            '',
            '',
            '',
            self.stock_count,
            current_stock_amount,
            current_cash_amount,
            total_amount,
            left_amount,
        ]
        self.report_list.append(report)

        with open(f"{self.output_path}_pessimistic_{trigger_line}_{factor}.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.report_list)


class AppendCallTool(Tool):

    daily_invest_amount = 40 * multiple
    smile_decline = 5
    invest_decline = 4.5

    report_headers = [
        'start date',
        'end date',
        'qqq decline',
        'invest amount',
        'stock quantity',
        'invest days',
        'income',
        'max invest amount',
        'total income',
    ]

    def __init__(self, qqq_data_source: ExIterator, output_path, data_source: ExIterator) -> None:
        super().__init__()
        self.qqq_data_source = qqq_data_source
        self.output_path = output_path
        self.data_source = data_source
        self.stock_count = 0
        self.qqq_smile: Smile = Smile(qqq_data_source)
        self.report_list: list[list] = [self.report_headers]
        self.report_data: list[str] = list()
        self.current_daily_price: DailyPrice = None
        self.invest_amount = 0
        self.invest_days = 0
        self.income = 0
        self.max_invest_amount = 0
        self.total_income = 0
        self.buy_sign = 0
        self.sell_sign = False

    def get_data_sources(self) -> set[ExIterator]:
        return {self.qqq_data_source, self.data_source}
    
    def execute(self):
        self.current_daily_price = self.data_source.current()
        qqq_sign = self.qqq_smile.forward()
        if self.buy_sign > 0:
            self._invest()
            self.buy_sign = 0
        if self.sell_sign:
            self.sell_sign = False
            self._clean()
            self._reset()

        if qqq_sign is SmileSignEnum.RECOVERY_AND_START_NEW:
            self.sell_sign = True
            self.report_data[1] = self.qqq_smile.current.p_date.isoformat()
        else:
            if not self.qqq_smile.is_smiling and self.qqq_smile.current_decline > self.smile_decline:
                self.qqq_smile.set_smiling()
                self.report_data.append(self.qqq_smile.highest.p_date.isoformat())
                self.report_data.append('')
                self.report_data.append(self.qqq_smile.max_decline)

            if self.qqq_smile.is_smiling and self.qqq_smile.current_decline > self.invest_decline:
            # if self.qqq_smile.is_smiling:
                self.buy_sign = self._buy_factor()
                self.report_data[2] = self.qqq_smile.max_decline

    def _buy_factor(self) -> int:
        # return max(1, self.qqq_smile.current_decline / 10)
        return 1

    def _invest(self):
        price = self.current_daily_price.get_avg_price()
        amount = self.daily_invest_amount * self.buy_sign
        quantity = round(int(amount * 10000 / price) / 10000, 4)
        cost = quantity * price
        self.invest_amount += cost
        self.stock_count += quantity
        self.invest_days += 1

    def _clean(self):
        price = self.current_daily_price.get_avg_price()
        self.income = price * self.stock_count - self.invest_amount
        self.max_invest_amount = max(self.max_invest_amount, self.invest_amount)
        self.total_income += self.income
        self.report_data.append(self._revert_amount(self.invest_amount))
        self.report_data.append(self.stock_count)
        self.report_data.append(self.invest_days)
        self.report_data.append(self._revert_amount(self.income))
        self.report_data.append(self._revert_amount(self.max_invest_amount))
        self.report_data.append(self._revert_amount(self.total_income))
        self.report_list.append(self.report_data)

    def _revert_amount(self, amount) -> int:
        return round(amount / multiple)

    def _reset(self):
        self.stock_count = 0
        self.report_data = list()
        self.invest_amount = 0
        self.invest_days = 0
        self.income = 0

    def report(self) -> list[str]:
        with open(f"{self.output_path}_append_call.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.report_list)


class ProfitAccumulatedTool(Tool):

    daily_invest_amount = 40 * multiple
    smile_decline = 5
    invest_decline = 4.5

    report_headers = [
        'start date',
        'end date',
        'qqq decline',
        'invest amount',
        'invest days',
        'buyed stock quantity',
        'retention stock quantity',
        'deviation',
        'max invest amount',
        'total deviation',
        'total stock quantity',
        'real time price',
        'real time amount',
    ]

    def __init__(self, qqq_data_source: ExIterator, output_path, data_source: ExIterator) -> None:
        super().__init__()
        self.qqq_data_source = qqq_data_source
        self.output_path = output_path
        self.data_source = data_source
        self.stock_count = 0
        self.qqq_smile: Smile = Smile(qqq_data_source)
        self.report_list: list[list] = [self.report_headers]
        self.report_data: list[str] = list()
        self.current_daily_price: DailyPrice = None
        self.invest_amount = 0
        self.invest_days = 0
        self.buyed_stock_quantity = 0
        self.max_invest_amount = 0
        self.total_deviation = 0
        self.buy_sign = 0
        self.sell_sign = False

    def get_data_sources(self) -> set[ExIterator]:
        return {self.qqq_data_source, self.data_source}
    
    def execute(self):
        self.current_daily_price = self.data_source.current()
        qqq_sign = self.qqq_smile.forward()
        if self.buy_sign > 0:
            self._invest()
            self.buy_sign = 0
        if self.sell_sign:
            self.sell_sign = False
            self._sell_out()
            self._reset()

        if qqq_sign is SmileSignEnum.RECOVERY_AND_START_NEW:
            self.sell_sign = True
            self.report_data[1] = self.qqq_smile.current.p_date.isoformat()
        else:
            if not self.qqq_smile.is_smiling and self.qqq_smile.current_decline > self.smile_decline:
                self.qqq_smile.set_smiling()
                self.report_data.append(self.qqq_smile.highest.p_date.isoformat())
                self.report_data.append('')
                self.report_data.append(self.qqq_smile.max_decline)

            # if self.qqq_smile.is_smiling and self.qqq_smile.current_decline > self.invest_decline:
            if self.qqq_smile.is_smiling:
                self.buy_sign = self._buy_factor()
                self.report_data[2] = self.qqq_smile.max_decline

    def _buy_factor(self) -> int:
        return max(1, self.qqq_smile.current_decline / 15)
        # return 1

    def _invest(self):
        price = self.current_daily_price.get_avg_price()
        amount = self.daily_invest_amount * self.buy_sign
        quantity = round(int(amount * 10000 / price) / 10000, 4)
        cost = quantity * price
        self.invest_amount += cost
        self.stock_count += quantity
        self.buyed_stock_quantity += quantity
        self.invest_days += 1

    def _sell_out(self):
        price = self.current_daily_price.get_avg_price()
        quantity = round(int(self.invest_amount * 10000 / price) / 10000, 4)
        deviation = self.invest_amount - quantity * price
        self.total_deviation += deviation
        self.stock_count -= quantity
        self.max_invest_amount = max(self.max_invest_amount, self.invest_amount)
        self.report_data.append(self._revert_amount(self.invest_amount))
        self.report_data.append(self.invest_days)
        self.report_data.append(self.buyed_stock_quantity)
        self.report_data.append(self.buyed_stock_quantity - quantity)
        self.report_data.append(self._revert_amount(deviation))
        self.report_data.append(self._revert_amount(self.max_invest_amount))
        self.report_data.append(self._revert_amount(self.total_deviation))
        self.report_data.append(self.stock_count)
        self.report_data.append(self._revert_amount(price, 2))
        self.report_data.append(self._revert_amount(self.stock_count * price))
        self.report_list.append(self.report_data)

    def _revert_amount(self, amount, ndigits=0) -> int:
        return round(amount / multiple, ndigits)

    def _reset(self):
        self.report_data = list()
        self.invest_amount = 0
        self.invest_days = 0
        self.buyed_stock_quantity = 0

    def report(self) -> list[str]:
        price = self.current_daily_price.get_avg_price()
        self.report_data.append(self.current_daily_price.p_date.isoformat())
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append('')
        self.report_data.append(self.stock_count)
        self.report_data.append(self._revert_amount(price, 2))
        self.report_data.append(self._revert_amount(self.stock_count * price))
        self.report_list.append(self.report_data)

        with open(f"{self.output_path}_profit_accumulated.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.report_list)


