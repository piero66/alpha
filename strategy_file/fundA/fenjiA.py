from rqalpha.api import *
from ext_utils import emailsender, insert_2_txt
from rqalpha.environment import Environment
from rqalpha.mod.rqalpha_mod_sys_stock_realtime.utils import get_tick, order_book_id_2_tushare_code


def init(context):
	context.fundA_list = {}
	context.target_doc = {}
	
	context.flag_down = -5.0

	context.receivers = ["623486086@qq.com", "297998119@qq.com"]
	context.logFileName = 'log_info.txt'
	
	
def before_trading(context):
	context.fundA_list = get_fund_a()


def get_fund_a():
	env = Environment.get_instance()
	order_book_id_list = sorted(
		[instruments.order_book_id for instruments in env.data_proxy.all_instruments("FenjiA", env.trading_dt)])
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
	context.fundA_list = get_fund_a()
	for fund in context.fundA_list:
		fund1 = order_book_id_2_tushare_code(fund)
		tick = get_tick(fund1, 'sina')
		now = tick[fund]['close']
		close = tick[fund]['prev_close']
		# 涨跌幅
		temp = round((now - close)/close * 100, 2)
		if temp <= context.flag_down:
			if fund not in context.target_doc:
				context.target_doc[fund] = [False, temp, now, close]
			elif temp != context.target_doc[fund][1]:
				context.target_doc[fund] = [False, temp, now, close]
		else:
			if fund in context.target_doc:
				context.target_doc.pop(fund)
				
	print(context.target_doc)
	for fund, data in context.target_doc.items():
		if not data[0]:
			info = "fund_id:" + fund + "  涨跌幅(%):" + str(data[1]) + "  now:" + str(data[2]) + "  close:" + str(data[3]) + "\n"
			emailsender(context.receivers, info, 'fenjiA')
			insert_2_txt(context.logFileName, info)
			data[0] = True
			context.target_doc[fund] = data
			
	

