# -*- coding: utf-8 -*-

from tool import Tool
from ex_iterator import ExIterator
from daily_price import DailyPrice
from enum import Enum, auto
from drawdown import DrawdownStage, calculate_decline
import csv


class PriceSign(Enum):
    INIT = auto()
    NEW_LOWEST = auto()
    RECOVERY = auto()
    TREND = auto()

class Smile:

    def __init__(self) -> None:
        self.highest: DailyPrice = None
        self.lowest: DailyPrice = None
        self.max_decline = None
        self.start: DailyPrice = None
        self.end: DailyPrice = None
        self.days: list[DailyPrice] = None
        self.is_smiling: bool = False
        self.drawdown_count: dict[DrawdownStage, int] = dict()

    def add(self, daily_price: DailyPrice) -> PriceSign:
        if self.highest is None or (not self._is_smiling() and daily_price.p_high > self.highest.p_high):
            self._init(daily_price)
            return PriceSign.INIT

        (decline, stage) = calculate_decline(self.highest.p_high, daily_price.p_low)
        is_smiling = self._is_smiling(decline)

        self.days.append(daily_price)
        if is_smiling and daily_price.p_low >= self.highest.p_high:
            self.end = daily_price
            return PriceSign.RECOVERY
        
        stage_count = self.drawdown_count.get(stage, 0)
        self.drawdown_count[stage] = stage_count + 1
        if daily_price.p_low < self.lowest.p_low:
            self.lowest = daily_price
            self.max_decline = decline
            sign = PriceSign.NEW_LOWEST
        else:
            sign = PriceSign.TREND
        
        return sign

    def _init(self, daily_price: DailyPrice):
        (decline, stage) = calculate_decline(daily_price.p_high, daily_price.p_low)
        self.highest = daily_price
        self.lowest = daily_price
        self.max_decline = decline
        self.start = daily_price
        self.days = [daily_price]
        self.drawdown_count = dict()
        self.drawdown_count[stage] = 1
        self._is_smiling(decline)

    def _is_smiling(self, decline = 0) -> bool:
        if self.is_smiling:
            return True
        elif decline >= 8.5:
            self.is_smiling = True
            return True
        else:
            return False


class QLDBearMarketTool(Tool):

    def __init__(self, data_source: ExIterator, output_path) -> None:
        super().__init__()
        self.data_source = data_source
        self.output_path = output_path
        self.smiles: list[Smile] = list()
        self.smile: Smile = Smile()

    def get_data_sources(self) -> set[ExIterator]:
        return set([self.data_source])

    def execute(self):
        current_daily_price = self.data_source.current()
        sign = self.smile.add(current_daily_price)
        if sign == PriceSign.RECOVERY:
                self.smiles.append(self.smile)
                self.smile = Smile()
                self.smile.add(current_daily_price)

    def report(self) -> list[str]:
        report_list = list()
        report_list.append(self._header)
        for smile in self.smiles:
            lowest_index = smile.days.index(smile.lowest)
            length = len(smile.days)

            report_row = [
                smile.start.p_date.isoformat(),
                smile.lowest.p_date.isoformat(),
                lowest_index + 1,
                smile.end.p_date.isoformat(),
                length - lowest_index - 1,
                length,
                f"{smile.max_decline}%",
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_0_5, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_5_10, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_10_15, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_15_20, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_20_25, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_25_30, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_30_35, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_35_40, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_40_45, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_45_50, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_50_55, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_55_60, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_60_65, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_65_70, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_70_75, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_75_80, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_80_85, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_85_90, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_90_95, 0),
                smile.drawdown_count.get(DrawdownStage.DRAWDOWN_OTHERS, 0),
            ]
            report_list.append(report_row)

        with open(self.output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(report_list)

    _header = [
        'Start', 
        'End', 
        'Drawdown Time', 
        'Recovery', 
        'Recovery Time', 
        'Underwater Period',
        'Drawdown',
        DrawdownStage.DRAWDOWN_0_5.value,
        DrawdownStage.DRAWDOWN_5_10.value,
        DrawdownStage.DRAWDOWN_10_15.value,
        DrawdownStage.DRAWDOWN_15_20.value,
        DrawdownStage.DRAWDOWN_20_25.value,
        DrawdownStage.DRAWDOWN_25_30.value,
        DrawdownStage.DRAWDOWN_30_35.value,
        DrawdownStage.DRAWDOWN_35_40.value,
        DrawdownStage.DRAWDOWN_40_45.value,
        DrawdownStage.DRAWDOWN_45_50.value,
        DrawdownStage.DRAWDOWN_50_55.value,
        DrawdownStage.DRAWDOWN_55_60.value,
        DrawdownStage.DRAWDOWN_60_65.value,
        DrawdownStage.DRAWDOWN_65_70.value,
        DrawdownStage.DRAWDOWN_70_75.value,
        DrawdownStage.DRAWDOWN_75_80.value,
        DrawdownStage.DRAWDOWN_80_85.value,
        DrawdownStage.DRAWDOWN_85_90.value,
        DrawdownStage.DRAWDOWN_90_95.value,
        DrawdownStage.DRAWDOWN_OTHERS.value,
    ]

