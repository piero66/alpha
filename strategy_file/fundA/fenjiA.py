from rqalpha.api import *
from rqalpha.mod.rqalpha_mod_sys_stock_realtime.data_board import realtime_tick, realtime_quotes_df
from ext_utils import get_fundamental, get_tick, emailsender, insert_2_text
from rqalpha.environment import Environment
from rqalpha.mod.rqalpha_mod_sys_stock_realtime.utils import get_tick, order_book_id_2_tushare_code

def init(context):

	context.fundA_list = {}
	context.receivers = ["623486086@qq.com"]

def before_trading(context):
	context.fundA_list = get_fund_a()

def get_fund_a():
	order_book_id_list = sorted(Environment.get_instance().data_proxy.all_instruments("FenjiA").order_book_id.tolist())
	code_list = [order_book_id_2_tushare_code(code) for code in order_book_id_list]
	realtime_tick = get_tick(code_list, 'sina')
	v_list = {k: v for k, v in realtime_tick.items() if v['volume'] > 50000}
	
	t_list = {}
	for code, data in v_list.items():
		t_list[code] = data['volume']
	f_list = sorted(t_list.items(), key=lambda x: x[1], reverse=False)
	t_list = []
	for k, v in f_list:
		t_list.append(k)
	return t_list

def handle_bar(context, bar_dict):
	# 开始编写你的主要的算法逻辑
	# bar_dict[order_book_id] 可以拿到某个证券的bar信息
	# context.portfolio 可以拿到现在的投资组合状态信息
	context.fundA_list = get_fund_a()
	for fund in context.fundA_list:
		fund1 = order_book_id_2_tushare_code(fund)
		tick = get_tick(fund1, 'sina')
		now = tick[fund]['close']
		close = tick[fund]['prev_close']
		# 涨跌幅
		temp = round((now - close)/close * 100, 2)
		if temp <= -5:
			info = fund + '  ' + "now:" + str(now) + "close:" + str(close) + "涨跌幅（%）：" + str(temp)
			emailsender(context.receivers, info, 'fenjiA')
	

