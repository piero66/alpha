from rqalpha.api import *
from rqalpha.mod.rqalpha_mod_sys_stock_realtime.data_board import realtime_tick, realtime_quotes_df
from ext_utils import get_fundamental, get_tick
def init(context):
	context.s1 = '600104.XSHG'
	context.s2 = '000895.XSHE'
	context.m1 = '162411.XSHE'
	
	context.stocks = {context.s1, context.s2}

def handle_bar(context, bar_dict):
	# 开始编写你的主要的算法逻辑
	# bar_dict[order_book_id] 可以拿到某个证券的bar信息
	# context.portfolio 可以拿到现在的投资组合状态信息
	# 查询持仓
	# print(context.portfolio.positions[context.s1])
	# print(context.portfolio.positions[context.s2])
	
	# 使用history_bars(book_order_id, mount, frequency, 'tick')方法进行数据获取
	
	
	# 获取历史数据
	hisdata_h = history_bars(context.s1, 130, '1d', 'high')
	#logger.info(hisdata_h)
	
	# 获取财务数据 仅支持 市值 PE PB
	search_value = {
		'maxMarket_cap': 50,
		'minMarket_cap': 0,
		'maxPE': None,
		'minPE': 0,
		'maxPB': None,
		'minPB': None,
		'sort': 'total_market_value',
	}
	
	value = get_fundamental(search_value)
	#print(value[:5])
	
	zs2 = '000016.XSHG'  # 上证50指数
	zs8 = '399333.XSHE'  # 创业板指数
	#print(bar_dict)
	his = history_bars(zs2, 20, '1d', 'close')
	his2 = history_bars(zs8, 20, '1d', 'close')
	#print(his)
	#print(his2)
	#ret2 = bar_dict[zs2]['close'] / his[0] - 1
	#ret8 = bar_dict[zs8]['close'] / his2[0] - 1
	print(history_bars(context.stocks, 2, '1d', 'close'))
	
	#print(bar_dict[zs8])
	
	
	# price = history_bars(context.m1, 1, '1m', 'tick')
	# logger.info(price['prev_close'])