# -*- coding: utf-8 -*-

from data_reader import DataReader
from tool_executory import ToolExecutory
from ex_iterator import ExIterator
from bear_market_tool import BearMarketTool
from tqqq_bear_market_tool import TQQQBearMarketTool
from qld_bear_market_tool import QLDBearMarketTool
from rebalance_tool import RebalanceTool, AppendCallTool, ProfitAccumulatedTool


data_root_path = 'E:\\my_projects\\price_go\\data\\'
# spy_data_path = data_root_path + 'SPY.csv'
# qqq_data_path = data_root_path + 'QQQ.csv'
# tqqq_data_path = data_root_path + 'TQQQ.csv'
# qld_data_path = data_root_path + 'QLD.csv'
spy_data_path = data_root_path + 'SPY_2011.csv'
qqq_data_path = data_root_path + 'QQQ_2011.csv'
tqqq_data_path = data_root_path + 'TQQQ_2011.csv'
qqq_long_data_path = data_root_path + 'QQQ_2007.csv'
qld_long_data_path = data_root_path + 'QLD_2007.csv'
qqq_all_data_path = data_root_path + 'QQQ.csv'

output_root_path = 'E:\\my_projects\\price_go\\output\\'
spy_bear_market_path = output_root_path + 'spy_bear_market.csv'
qqq_bear_market_path = output_root_path + 'qqq_bear_market.csv'
tqqq_bear_market_path = output_root_path + 'tqqq_bear_market.csv'
qld_bear_market_path = output_root_path + 'qld_bear_market.csv'
tqqq_rebalance_path = output_root_path + 'tqqq_rebalance'
qld_profit_path = output_root_path + 'qld_profit'
qqq_profit_path = output_root_path + 'qqq_profit'

data_reader = DataReader()
spy_history_prices = data_reader.make_history_prices(spy_data_path)
qqq_history_prices = data_reader.make_history_prices(qqq_data_path)
tqqq_history_prices = data_reader.make_history_prices(tqqq_data_path)
# qld_history_prices = data_reader.make_history_prices(qld_data_path)
qqq_long_history_prices = data_reader.make_history_prices(qqq_long_data_path)
qld_long_history_prices = data_reader.make_history_prices(qld_long_data_path)
qqq_all_history_prices = data_reader.make_history_prices(qqq_all_data_path)

spy_iter = ExIterator(iter(spy_history_prices.daily_price_list))
qqq_iter = ExIterator(iter(qqq_history_prices.daily_price_list))
tqqq_iter = ExIterator(iter(tqqq_history_prices.daily_price_list))
# qld_iter = ExIterator(iter(qld_history_prices.daily_price_list))
qqq_long_iter = ExIterator(iter(qqq_long_history_prices.daily_price_list))
qld_long_iter = ExIterator(iter(qld_long_history_prices.daily_price_list))
qqq_all_iter = ExIterator(iter(qqq_all_history_prices.daily_price_list))

# spy_bear_market_tool = BearMarketTool(spy_iter, spy_bear_market_path)
# qqq_bear_market_tool = BearMarketTool(qqq_iter, qqq_bear_market_path)
# tqqq_bear_market_tool = TQQQBearMarketTool(tqqq_iter, tqqq_bear_market_path)
# qld_bear_market_tool = QLDBearMarketTool(qld_iter, qld_bear_market_path)
# rebalance_tool = RebalanceTool(spy_iter, qqq_iter, tqqq_rebalance_path, tqqq_iter, 15000, 0)
# append_call_tool = AppendCallTool(qqq_iter, tqqq_rebalance_path, tqqq_iter)
# profit_accumulated_tool = ProfitAccumulatedTool(qqq_iter, tqqq_rebalance_path, tqqq_iter)
# profit_accumulated_tool = ProfitAccumulatedTool(qqq_long_iter, qld_profit_path, qld_long_iter)
profit_accumulated_tool = ProfitAccumulatedTool(qqq_all_iter, qqq_profit_path, qqq_all_iter)

tool_executory = ToolExecutory()
#tool_executory.add_tool(spy_bear_market_tool)
#tool_executory.add_tool(qqq_bear_market_tool)
#tool_executory.add_tool(tqqq_bear_market_tool)
# tool_executory.add_tool(qld_bear_market_tool)
# tool_executory.add_tool(rebalance_tool)
# tool_executory.add_tool(append_call_tool)
tool_executory.add_tool(profit_accumulated_tool)

tool_executory.execute()
tool_executory.report()
