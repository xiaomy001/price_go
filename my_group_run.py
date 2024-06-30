# -*- coding: utf-8 -*-


from data_reader import DataReader
from daily_price import DailyPrice
from history_prices import HistoryPrices
import csv

data_root_path = 'E:\\my_projects\\price_go\\data\\'
qqq_2000_data_path = data_root_path + 'QQQ-2000_2004.csv'
qqq_2005_data_path = data_root_path + 'QQQ-2005_2024.csv'
brk_2000_data_path = data_root_path + 'BRK-B-2000_2004.csv'
brk_2005_data_path = data_root_path + 'BRK-B-2005_2024.csv'
sgcta_2000_data_path = data_root_path + 'SGCTA-2000_2004.csv'
sgcta_2005_data_path = data_root_path + 'SGCTA-2005_2024.csv'
gold_2000_data_path = data_root_path + 'GOLD-2000_2004.csv'
iau_2005_data_path = data_root_path + 'IAU-2005_2024.csv'
tlt_2005_data_path = data_root_path + 'TLT-2005_2024.csv'

output_root_path = 'E:\\my_projects\\price_go\\output\\'
my_2000_drawdown_summary_path = output_root_path + 'my_drawdown_summary_2000.csv'
my_2000_balance_summary_path = output_root_path + 'my_balance_summary_2000.csv'
my_2000_annualized_summary_path = output_root_path + 'my_annualized_summary_2000.csv'
my_2000_detail_path = output_root_path + 'my_detail_2000.csv'
my_2005_drawdown_summary_path = output_root_path + 'my_drawdown_summary_2005.csv'
my_2005_balance_summary_path = output_root_path + 'my_balance_summary_2005.csv'
my_2005_annualized_summary_path = output_root_path + 'my_annualized_summary_2005.csv'
my_2005_detail_path = output_root_path + 'my_detail_2005.csv'

data_reader = DataReader()
qqq_2000_history_prices: HistoryPrices = data_reader.make_history_prices(qqq_2000_data_path)
qqq_2005_history_prices: HistoryPrices = data_reader.make_history_prices(qqq_2005_data_path)
brk_2000_history_prices: HistoryPrices = data_reader.make_history_prices(brk_2000_data_path)
brk_2005_history_prices: HistoryPrices = data_reader.make_history_prices(brk_2005_data_path)
sgcta_2000_history_prices: HistoryPrices = data_reader.make_history_prices(sgcta_2000_data_path)
sgcta_2005_history_prices: HistoryPrices = data_reader.make_history_prices(sgcta_2005_data_path)
gold_2000_history_prices: HistoryPrices = data_reader.make_history_prices(gold_2000_data_path)
iau_2005_history_prices: HistoryPrices = data_reader.make_history_prices(iau_2005_data_path)
tlt_2005_history_prices: HistoryPrices = data_reader.make_history_prices(tlt_2005_data_path)

report_drawdown_summary_headers = [
    'Start Date',
    'Inflection Point Date',
    'End Date',
    'Drawdown Time',
    'Recovery Time',
    'Underwater Durations',
    'Drawdown',
    f'0%-5%',
    f'5%-10%',
    f'10%-15%',
    f'15%-20%',
    f'20%-25%',
    f'25%-30%',
    f'30%-35%',
    f'35%-40%',
    f'40%-45%',
    f'45%-50%',
    'others',
]

report_balance_summary_headers = [
    'Balance Date',
    'QQQ Weight(Before)',
    'BRK Weight(Before)',
    'CTA Weight(Before)',
    'GOLD Weight(Before)',
    'TLT Weight(Before)',
    'Total Amount',
    'Semi-Annualized Return',
    'Total Return',
]

report_annualized_summary_headers = [
    'Start Date',
    'End Date',
    'Total Amount',
    'Annualized Return',
    'Total Return',
    # 'Total Expense',
]

report_detail_headers = [
    'Date',
    'Stock Amount',
    'Total Amount',
]

drawdown_summary_list: list[list] = [report_drawdown_summary_headers]
drawdown_summary: list = list()
balance_summary_list: list[list] = [report_balance_summary_headers]
balance_summary: list = list()
annualized_summary_list: list[list] = [report_annualized_summary_headers]
annualized_summary: list = list()
detail_list: list[list] = [report_detail_headers]

multiple = 1000000
cash_multiple = 10000
cash = 10000 * cash_multiple * multiple
remaining_cash = cash
qqq_quatity = 0
brk_quatity = 0
cta_quatity = 0
gold_quatity = 0
tlt_quatity = 0

init = False
def calculate_stock_change(amount, price) -> int:
    return int(amount / price)

def calculate_total_stocks_amount(qqq_price, brk_price, cta_price, gold_price) -> int:
    global qqq_quatity
    global brk_quatity
    global cta_quatity
    global gold_quatity
    return qqq_price * qqq_quatity + brk_price * brk_quatity + cta_price * cta_quatity + gold_price * gold_quatity

def calcualte_total_amount(qqq_price, brk_price, cta_price, gold_price) -> int:
    global remaining_cash
    return calculate_total_stocks_amount(qqq_price, brk_price, cta_price, gold_price) + remaining_cash

def balance_stocks(qqq_price, brk_price, cta_price, gold_price):
    global qqq_quatity
    global brk_quatity
    global cta_quatity
    global gold_quatity
    global remaining_cash
    total_amount = calcualte_total_amount(qqq_price, brk_price, cta_price, gold_price)
    # qqq_amount = total_amount * 0.25
    brk_amount = total_amount * 0.25
    cta_amount = total_amount * 0.25
    gold_amount = total_amount * 0.25
    # qqq_quatity = calculate_stock_change(qqq_amount, qqq_price)
    brk_quatity = calculate_stock_change(brk_amount, brk_price)
    cta_quatity = calculate_stock_change(cta_amount, cta_price)
    gold_quatity = calculate_stock_change(gold_amount, gold_price)
    qqq_quatity = calculate_stock_change(total_amount - gold_quatity * gold_price - brk_quatity * brk_price - cta_quatity * cta_price, qqq_price)
    remaining_cash = total_amount - qqq_quatity * qqq_price - brk_quatity * brk_price - cta_quatity * cta_price - gold_quatity * gold_price

highest = 0
lowest = 0
drawdown_records = dict()
left_days = 0
right_days = 0
year_begin_amount = 0
pre_balance_amount = 0
pre_balance_month = 2
i = 0
count = len(qqq_2000_history_prices.daily_price_list)
while i < count:
    qqq_daily_price: DailyPrice = qqq_2000_history_prices.daily_price_list[i]
    i += 1

    if init and not len(annualized_summary) == 0 and not annualized_summary[0].year == qqq_daily_price.p_date.year:
        annualized_summary[0] = annualized_summary[0].isoformat()
        annualized_summary.append(today)
        annualized_summary.append(total_amount / cash_multiple / multiple)
        annualized_summary.append(round((total_amount - year_begin_amount) / year_begin_amount, 4))
        annualized_summary.append(round((total_amount - cash) / cash, 4))
        annualized_summary_list.append(annualized_summary)
        annualized_summary = list()

    today_price = qqq_daily_price.p_date
    today = qqq_daily_price.p_date.isoformat()

    qqq_price = qqq_daily_price.p_close
    brk_index = brk_2000_history_prices.date_index.get(today, None)
    cta_index = sgcta_2000_history_prices.date_index.get(today, None)
    gold_index = gold_2000_history_prices.date_index.get(today, None)

    if None in {brk_index, cta_index, gold_index}:
        print(f"{today}: {brk_index}, {cta_index}, {gold_index}")
        continue

    brk_price = brk_2000_history_prices.daily_price_list[brk_index].p_close
    cta_price = sgcta_2000_history_prices.daily_price_list[cta_index].p_close
    gold_price = gold_2000_history_prices.daily_price_list[gold_index].p_close

    if not init:
        balance_stocks(qqq_price, brk_price, cta_price, gold_price)
        annualized_summary.append(today_price)
        year_begin_amount = cash
        pre_balance_amount = cash
        init = True

    stock_amount = calculate_total_stocks_amount(qqq_price, brk_price, cta_price, gold_price)
    total_amount = calcualte_total_amount(qqq_price, brk_price, cta_price, gold_price)
    detail_list.append([today, round(stock_amount / cash_multiple / multiple, 4), round(total_amount / cash_multiple / multiple, 4)])

    if len(annualized_summary) == 0:
        annualized_summary.append(today_price)
        year_begin_amount = total_amount

    if len(drawdown_summary) == 0:
        drawdown_summary = [today, today, today]
        highest = stock_amount
        lowest = stock_amount
    else:
        if stock_amount >= highest:
            if highest * 0.95 >= lowest:
                drawdown_summary[2] = today
                drawdown_summary.append(left_days)
                drawdown_summary.append(right_days)
                drawdown_summary.append(left_days + right_days)
                drawdown_summary.append(round((highest - lowest) / highest, 4))
                drawdown_summary.append(drawdown_records.get(0, 0)) # 0-5
                drawdown_summary.append(drawdown_records.get(1, 0)) # 5-10
                drawdown_summary.append(drawdown_records.get(2, 0)) # 10-15
                drawdown_summary.append(drawdown_records.get(3, 0)) # 15-20
                drawdown_summary.append(drawdown_records.get(4, 0)) # 20-25
                drawdown_summary.append(drawdown_records.get(5, 0)) # 25-30
                drawdown_summary.append(drawdown_records.get(6, 0)) # 30-35
                drawdown_summary.append(drawdown_records.get(7, 0)) # 35-40
                drawdown_summary.append(drawdown_records.get(8, 0)) # 40-45
                drawdown_summary.append(drawdown_records.get(9, 0)) # 45-50
                drawdown_summary.append(drawdown_records.get(10, 0)) # 50-100
                drawdown_summary_list.append(drawdown_summary)
            drawdown_summary = [today, today, today]
            highest = stock_amount
            lowest = stock_amount
            drawdown_records = dict()
            left_days = 0
            right_days = 0
        else:
            if stock_amount <= lowest:
                drawdown_summary[1] = today
                drawdown_summary[2] = today
                lowest = stock_amount
                left_days += right_days + 1
                right_days = 0
            else:
                drawdown_summary[2] = today
                right_days += 1
            index = int((highest - stock_amount) * 100 / highest / 5)
            if index > 9:
                drawdown_records[10] = drawdown_records.get(10, 0) + 1
            else:
                drawdown_records[index] = drawdown_records.get(index, 0) + 1

    month = today_price.month
    if len(balance_summary) == 0 and (month in (2, 8) and not month == pre_balance_month):
        balance_summary.append(today)
        balance_summary.append(round(qqq_quatity * qqq_price / stock_amount, 3))
        balance_summary.append(round(brk_quatity * brk_price / stock_amount, 3))
        balance_summary.append(round(cta_quatity * cta_price / stock_amount, 3))
        balance_summary.append(round(gold_quatity * gold_price / stock_amount, 3))
        balance_summary.append(0)
        balance_summary.append(round(total_amount / cash_multiple / multiple, 4))
        balance_summary.append(round((total_amount - pre_balance_amount) / pre_balance_amount, 4))
        balance_summary.append(round((total_amount - cash) / cash, 4))
        balance_summary_list.append(balance_summary)
        pre_balance_month = 10 - pre_balance_month
        pre_balance_amount = total_amount
        balance_summary = list()
        balance_stocks(qqq_price, brk_price, cta_price, gold_price)

if len(drawdown_summary) == 3 and left_days > 0:
    drawdown_summary[2] = today
    drawdown_summary.append(left_days)
    drawdown_summary.append(f"> {right_days}")
    drawdown_summary.append(f"> {left_days + right_days}")
    drawdown_summary.append(round((highest - lowest) / highest, 4))
    drawdown_summary.append(drawdown_records.get(0, 0)) # 0-5
    drawdown_summary.append(drawdown_records.get(1, 0)) # 5-10
    drawdown_summary.append(drawdown_records.get(2, 0)) # 10-15
    drawdown_summary.append(drawdown_records.get(3, 0)) # 15-20
    drawdown_summary.append(drawdown_records.get(4, 0)) # 20-25
    drawdown_summary.append(drawdown_records.get(5, 0)) # 25-30
    drawdown_summary.append(drawdown_records.get(6, 0)) # 30-35
    drawdown_summary.append(drawdown_records.get(7, 0)) # 35-40
    drawdown_summary.append(drawdown_records.get(8, 0)) # 40-45
    drawdown_summary.append(drawdown_records.get(9, 0)) # 45-50
    drawdown_summary.append(drawdown_records.get(10, 0)) # 50-100
    drawdown_summary_list.append(drawdown_summary)

if not len(annualized_summary) == 0:
    annualized_summary.append(today)
    annualized_summary.append(round(total_amount / cash_multiple / multiple, 4))
    annualized_summary.append(round((total_amount - year_begin_amount) / year_begin_amount, 4))
    annualized_summary.append(round((total_amount - cash) / cash, 4))
    annualized_summary_list.append(annualized_summary)

with open(my_2000_drawdown_summary_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(drawdown_summary_list)

with open(my_2000_balance_summary_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(balance_summary_list)

with open(my_2000_annualized_summary_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(annualized_summary_list)

with open(my_2000_detail_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(detail_list)



drawdown_summary_list: list[list] = [report_drawdown_summary_headers]
drawdown_summary: list = list()
balance_summary_list: list[list] = [report_balance_summary_headers]
balance_summary: list = list()
annualized_summary_list: list[list] = [report_annualized_summary_headers]
annualized_summary: list = list()
detail_list: list[list] = [report_detail_headers]

multiple = 1000000
cash_multiple = 10000
cash = 10000 * cash_multiple * multiple
remaining_cash = cash
qqq_quatity = 0
brk_quatity = 0
cta_quatity = 0
gold_quatity = 0
tlt_quatity = 0

init = False

def calculate_total_stocks_amount_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price) -> int:
    global qqq_quatity
    global brk_quatity
    global cta_quatity
    global gold_quatity
    global tlt_quatity
    return qqq_price * qqq_quatity + brk_price * brk_quatity + cta_price * cta_quatity + gold_price * gold_quatity + tlt_price * tlt_quatity

def calcualte_total_amount_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price) -> int:
    global remaining_cash
    return calculate_total_stocks_amount_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price) + remaining_cash

def balance_stocks_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price):
    global qqq_quatity
    global brk_quatity
    global cta_quatity
    global gold_quatity
    global tlt_quatity
    global remaining_cash
    total_amount = calcualte_total_amount_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price)
    # qqq_amount = total_amount * 0.25
    brk_amount = total_amount * 0.2
    # cta_amount = total_amount * 0.25
    gold_amount = total_amount * 0.3
    tlt_amount = total_amount * 0.2
    # qqq_quatity = calculate_stock_change(qqq_amount, qqq_price)
    brk_quatity = calculate_stock_change(brk_amount, brk_price)
    # cta_quatity = calculate_stock_change(cta_amount, cta_price)
    gold_quatity = calculate_stock_change(gold_amount, gold_price)
    tlt_quatity = calculate_stock_change(tlt_amount, tlt_price)
    qqq_quatity = calculate_stock_change(total_amount - gold_quatity * gold_price - tlt_quatity * tlt_price - brk_quatity * brk_price - cta_quatity * cta_price, qqq_price)
    remaining_cash = total_amount - qqq_quatity * qqq_price - brk_quatity * brk_price - cta_quatity * cta_price - gold_quatity * gold_price - tlt_quatity * tlt_price

highest = 0
lowest = 0
drawdown_records = dict()
left_days = 0
right_days = 0
year_begin_amount = 0
pre_balance_amount = 0
pre_balance_month = 2
i = 0
count = len(qqq_2005_history_prices.daily_price_list)
while i < count:
    qqq_daily_price: DailyPrice = qqq_2005_history_prices.daily_price_list[i]
    i += 1

    if init and not len(annualized_summary) == 0 and not annualized_summary[0].year == qqq_daily_price.p_date.year:
        annualized_summary[0] = annualized_summary[0].isoformat()
        annualized_summary.append(today)
        annualized_summary.append(total_amount / cash_multiple / multiple)
        annualized_summary.append(round((total_amount - year_begin_amount) / year_begin_amount, 4))
        annualized_summary.append(round((total_amount - cash) / cash, 4))
        annualized_summary_list.append(annualized_summary)
        annualized_summary = list()

    today_price = qqq_daily_price.p_date
    today = qqq_daily_price.p_date.isoformat()

    qqq_price = qqq_daily_price.p_close
    brk_index = brk_2005_history_prices.date_index.get(today, None)
    cta_index = sgcta_2005_history_prices.date_index.get(today, None)
    gold_index = iau_2005_history_prices.date_index.get(today, None)
    tlt_index = tlt_2005_history_prices.date_index.get(today, None)

    if None in {brk_index, cta_index, gold_index, tlt_index}:
        print(f"{today}: {brk_index}, {cta_index}, {gold_index}, {tlt_index}")
        continue

    brk_price = brk_2005_history_prices.daily_price_list[brk_index].p_close
    cta_price = sgcta_2005_history_prices.daily_price_list[cta_index].p_close
    gold_price = iau_2005_history_prices.daily_price_list[gold_index].p_close
    tlt_price = tlt_2005_history_prices.daily_price_list[tlt_index].p_close

    if not init:
        balance_stocks_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price)
        annualized_summary.append(today_price)
        year_begin_amount = cash
        pre_balance_amount = cash
        init = True

    stock_amount = calculate_total_stocks_amount_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price)
    total_amount = calcualte_total_amount_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price)
    detail_list.append([today, round(stock_amount / cash_multiple / multiple, 4), round(total_amount / cash_multiple / multiple, 4)])

    if len(annualized_summary) == 0:
        annualized_summary.append(today_price)
        year_begin_amount = total_amount

    if len(drawdown_summary) == 0:
        drawdown_summary = [today, today, today]
        highest = stock_amount
        lowest = stock_amount
    else:
        if stock_amount >= highest:
            if highest * 0.95 >= lowest:
                drawdown_summary[2] = today
                drawdown_summary.append(left_days)
                drawdown_summary.append(right_days)
                drawdown_summary.append(left_days + right_days)
                drawdown_summary.append(round((highest - lowest) / highest, 4))
                drawdown_summary.append(drawdown_records.get(0, 0)) # 0-5
                drawdown_summary.append(drawdown_records.get(1, 0)) # 5-10
                drawdown_summary.append(drawdown_records.get(2, 0)) # 10-15
                drawdown_summary.append(drawdown_records.get(3, 0)) # 15-20
                drawdown_summary.append(drawdown_records.get(4, 0)) # 20-25
                drawdown_summary.append(drawdown_records.get(5, 0)) # 25-30
                drawdown_summary.append(drawdown_records.get(6, 0)) # 30-35
                drawdown_summary.append(drawdown_records.get(7, 0)) # 35-40
                drawdown_summary.append(drawdown_records.get(8, 0)) # 40-45
                drawdown_summary.append(drawdown_records.get(9, 0)) # 45-50
                drawdown_summary.append(drawdown_records.get(10, 0)) # 50-100
                drawdown_summary_list.append(drawdown_summary)
            drawdown_summary = [today, today, today]
            highest = stock_amount
            lowest = stock_amount
            drawdown_records = dict()
            left_days = 0
            right_days = 0
        else:
            if stock_amount <= lowest:
                drawdown_summary[1] = today
                drawdown_summary[2] = today
                lowest = stock_amount
                left_days += right_days + 1
                right_days = 0
            else:
                drawdown_summary[2] = today
                right_days += 1
            index = int((highest - stock_amount) * 100 / highest / 5)
            if index > 9:
                drawdown_records[10] = drawdown_records.get(10, 0) + 1
            else:
                drawdown_records[index] = drawdown_records.get(index, 0) + 1

    month = today_price.month
    if len(balance_summary) == 0 and (month in (2, 8) and not month == pre_balance_month):
        balance_summary.append(today)
        balance_summary.append(round(qqq_quatity * qqq_price / stock_amount, 3))
        balance_summary.append(round(brk_quatity * brk_price / stock_amount, 3))
        balance_summary.append(round(cta_quatity * cta_price / stock_amount, 3))
        balance_summary.append(round(gold_quatity * gold_price / stock_amount, 3))
        balance_summary.append(round(tlt_quatity * tlt_price / stock_amount, 3))
        balance_summary.append(round(total_amount / cash_multiple / multiple, 4))
        balance_summary.append(round((total_amount - pre_balance_amount) / pre_balance_amount, 4))
        balance_summary.append(round((total_amount - cash) / cash, 4))
        balance_summary_list.append(balance_summary)
        pre_balance_month = 10 - pre_balance_month
        pre_balance_amount = total_amount
        balance_summary = list()
        balance_stocks_tlt(qqq_price, brk_price, cta_price, gold_price, tlt_price)

if len(drawdown_summary) == 3 and left_days > 0:
    drawdown_summary[2] = today
    drawdown_summary.append(left_days)
    drawdown_summary.append(f"> {right_days}")
    drawdown_summary.append(f"> {left_days + right_days}")
    drawdown_summary.append(round((highest - lowest) / highest, 4))
    drawdown_summary.append(drawdown_records.get(0, 0)) # 0-5
    drawdown_summary.append(drawdown_records.get(1, 0)) # 5-10
    drawdown_summary.append(drawdown_records.get(2, 0)) # 10-15
    drawdown_summary.append(drawdown_records.get(3, 0)) # 15-20
    drawdown_summary.append(drawdown_records.get(4, 0)) # 20-25
    drawdown_summary.append(drawdown_records.get(5, 0)) # 25-30
    drawdown_summary.append(drawdown_records.get(6, 0)) # 30-35
    drawdown_summary.append(drawdown_records.get(7, 0)) # 35-40
    drawdown_summary.append(drawdown_records.get(8, 0)) # 40-45
    drawdown_summary.append(drawdown_records.get(9, 0)) # 45-50
    drawdown_summary.append(drawdown_records.get(10, 0)) # 50-100
    drawdown_summary_list.append(drawdown_summary)

if not len(annualized_summary) == 0:
    annualized_summary.append(today)
    annualized_summary.append(round(total_amount / cash_multiple / multiple, 4))
    annualized_summary.append(round((total_amount - year_begin_amount) / year_begin_amount, 4))
    annualized_summary.append(round((total_amount - cash) / cash, 4))
    annualized_summary_list.append(annualized_summary)

with open(my_2005_drawdown_summary_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(drawdown_summary_list)

with open(my_2005_balance_summary_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(balance_summary_list)

with open(my_2005_annualized_summary_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(annualized_summary_list)

with open(my_2005_detail_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(detail_list)



