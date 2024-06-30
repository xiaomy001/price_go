# -*- coding: utf-8 -*-

from daily_price import DailyPrice
from enum import Enum, auto


class PriceSign(Enum):
    INIT = auto()
    TREND = auto()
    NEW_LOWEST = auto()
    RECOVERY = auto()


class SignCheck:

    def check(self, daily_price: DailyPrice) -> PriceSign:
        pass


class SmileCurve:

    def __init__(self, smiling_decline: float) -> None:
        self.highest: DailyPrice = None
        self.lowest: DailyPrice = None
        self.max_decline = None
        self.current_decline = None
        self.start: DailyPrice = None
        self.end: DailyPrice = None
        self.is_smiling: bool = False
        self.smiling_decline = smiling_decline
        self.sign_check_list: list[SignCheck] = list()

    def add(self, daily_price: DailyPrice) -> PriceSign:
        for sign_check in self.sign_check_list:
            sign = sign_check.check(daily_price)
            if not sign is None:
                return sign
        raise Exception()
    
    def init(self, daily_price: DailyPrice):
        pass

    def _is_smiling(self, decline = 0) -> bool:
        if self.is_smiling:
            return True
        elif decline >= self.smiling_decline:
            self.is_smiling = True
            return True
        else:
            return False


class _InitSignCheck(SignCheck):

    def __init__(self, smile_curve: SmileCurve) -> None:
        super().__init__()
        self.smile_curve = smile_curve

    def check(self, daily_price: DailyPrice) -> PriceSign:
        return super().check(daily_price)


class _TrendSignCheck(SignCheck):

    def __init__(self, smile_curve: SmileCurve) -> None:
        super().__init__()
        self.smile_curve = smile_curve

    def check(self, daily_price: DailyPrice) -> PriceSign:
        return super().check(daily_price)


class _NewLowestSignCheck(SignCheck):

    def __init__(self, smile_curve: SmileCurve) -> None:
        super().__init__()
        self.smile_curve = smile_curve

    def check(self, daily_price: DailyPrice) -> PriceSign:
        return super().check(daily_price)
    

class _RecoverySignCheck(SignCheck):

    def __init__(self, smile_curve: SmileCurve) -> None:
        super().__init__()
        self.smile_curve = smile_curve

    def check(self, daily_price: DailyPrice) -> PriceSign:
        return super().check(daily_price)


class RebalanceTriggerSmileCurve(SmileCurve):

    def __init__(self, smiling_decline: float) -> None:
        super().__init__(smiling_decline)

