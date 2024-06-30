# -*- coding: utf-8 -*-

from enum import Enum, auto


class DrawdownStage(Enum):
    DRAWDOWN_0_5 = f'0%-5%'
    DRAWDOWN_5_10 = f'5%-10%'
    DRAWDOWN_10_15 = f'10%-15%'
    DRAWDOWN_15_20 = f'15%-20%'
    DRAWDOWN_20_25= f'20%-25%'
    DRAWDOWN_25_30 = f'25%-30%'
    DRAWDOWN_30_35 = f'30%-35%'
    DRAWDOWN_35_40 = f'35%-40%'
    DRAWDOWN_40_45 = f'40%-45%'
    DRAWDOWN_45_50 = f'45%-50%'
    DRAWDOWN_50_55 = f'50%-55%'
    DRAWDOWN_55_60 = f'55%-60%'
    DRAWDOWN_60_65= f'60%-65%'
    DRAWDOWN_65_70 = f'65%-70%'
    DRAWDOWN_70_75 = f'70%-75%'
    DRAWDOWN_75_80 = f'75%-80%'
    DRAWDOWN_80_85 = f'80%-85%'
    DRAWDOWN_85_90 = f'85%-90%'
    DRAWDOWN_90_95 = f'90%-95%'
    DRAWDOWN_OTHERS = 'others'

def calculate_decline(highest_price, current_price) -> tuple[float, DrawdownStage]:
    diff = highest_price - current_price
    decline = round(diff * 100 / highest_price, 2)

    if decline < 5:
        stage = DrawdownStage.DRAWDOWN_0_5
    elif decline < 10:
        stage = DrawdownStage.DRAWDOWN_5_10
    elif decline < 15:
        stage = DrawdownStage.DRAWDOWN_10_15
    elif decline < 20:
        stage = DrawdownStage.DRAWDOWN_15_20
    elif decline < 25:
        stage = DrawdownStage.DRAWDOWN_20_25
    elif decline < 30:
        stage = DrawdownStage.DRAWDOWN_25_30
    elif decline < 35:
        stage = DrawdownStage.DRAWDOWN_30_35
    elif decline < 40:
        stage = DrawdownStage.DRAWDOWN_35_40
    elif decline < 45:
        stage = DrawdownStage.DRAWDOWN_40_45
    elif decline < 50:
        stage = DrawdownStage.DRAWDOWN_45_50
    elif decline < 55:
        stage = DrawdownStage.DRAWDOWN_50_55
    elif decline < 60:
        stage = DrawdownStage.DRAWDOWN_55_60
    elif decline < 65:
        stage = DrawdownStage.DRAWDOWN_60_65
    elif decline < 70:
        stage = DrawdownStage.DRAWDOWN_65_70
    elif decline < 75:
        stage = DrawdownStage.DRAWDOWN_70_75
    elif decline < 80:
        stage = DrawdownStage.DRAWDOWN_75_80
    elif decline < 85:
        stage = DrawdownStage.DRAWDOWN_80_85
    elif decline < 90:
        stage = DrawdownStage.DRAWDOWN_85_90
    elif decline < 95:
        stage = DrawdownStage.DRAWDOWN_90_95
    else:
        stage = DrawdownStage.DRAWDOWN_OTHERS

    return (decline, stage)


if __name__ == '__main__':
    print(calculate_decline(66500000, 63939999))
    print(str(DrawdownStage.DRAWDOWN_60_65.value))
