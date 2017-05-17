from rqalpha.api import *

import pandas as pd
from ext_utils import get_fundamental, get_tick, insert_2_text, emailsender

import numpy as np
from datetime import datetime, timedelta


def init(context):
	context.blackList = ['000594.XSHE', "600656.XSHG", "300372.XSHE", "600403.XSHG", "600421.XSHG", "600733.XSHG",
	                     "300399.XSHE",
	                     "600145.XSHG", "002679.XSHE", "000020.XSHE", "002330.XSHE", "300117.XSHE", "300135.XSHE",
	                     "002566.XSHE", "002119.XSHE", "300208a.XSHE", "002237.XSHE", "002608.XSHE", "000691.XSHE",
	                     "002694.XSHE", "002715.XSHE", "002211.XSHE", "000788.XSHE", "300380.XSHE", "300028.XSHE",
	                     "000668.XSHE", "300033.XSHE", "300126.XSHE", "300340.XSHE", "300344.XSHE", "002473.XSHE",
	                     '000707.XSHE']
	context.isFilterGem = True
	context.isSelectByEps = False
	context.total = 200
	context.period = 130
	context.tradePeriod = 1
	context.flag = -1
	context.holdSize = 8
	context.holdWeight = 0.125
	context.tgtOrder = {}
	context.isBuy = {}
	context.stocks1 = []
	context.stocks2 = []
	context.isSafe = True
	
	context.logFileName = 'log_info.txt'
	context.receivers = ['623486086@qq.com']

def before_trading(context, bar_dict):
	context.flag += 1
	if context.isSafe:
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
		context.stocks1 = value


	else:
		search_value = {
			'maxMarket_cap': 500,
			'minMarket_cap': 0,
			'maxPE': None,
			'minPE': None,
			'maxPB': 3,
			'minPB': 0,
			'sort': 'total_market_value',
		}
		value = get_fundamental(search_value)
		context.stocks2 = value[:5]
		context.stocks2 = [stk for stk in context.stocks2 if stk not in context.blackList]
		print('PB')
		print(context.stocks2)


def isSafe(bar_dict, context):
	zs2 = '000016.XSHG'  # 上证50指数
	zs8 = '399333.XSHE'  # 创业板指数
	his = history_bars(zs2, 20, '1d', 'close')
	his2 = history_bars(zs8, 20, '1d', 'close')
	close1 = bar_dict[zs2].close
	close2 = get_tick(zs8)[zs8]['close']
	ret2 = close1 / his[0] - 1
	ret8 = close2 / his2[0] - 1
	
	if ret2 < -0.02 and ret8 < -0.02:
		context.isSafe = False
		return False
	else:
		context.isSafe = True
		return True


def getScore(stkList, bar_dict, context):
	buyList = {}
	for stk in stkList:
		close = history_bars(stk, 130, '1d', 'close')
		low = history_bars(stk, 130, '1d', 'low')
		high = history_bars(stk, 130, '1d', 'high')
		highPrice = high.max()
		lowPrice = low.min()
		
		'''FIX ME'''  # 可能有问题
		avg15 = history_bars(stk, 15, '1d', 'close').mean()
		
		curPrice = history_bars(stk, 1, '1d', 'tick')['close']
		score = curPrice * 3 - highPrice - lowPrice - avg15
		buyList[stk] = score
	
	# dfs = pd.DataFrame(buyList.values, index=buyList.keys)
	dfs = pd.Series(buyList)
	dfs = pd.DataFrame(dfs)
	dfs = dfs.sort(columns=0, ascending=True)
	return list(dfs.index)


def filterGem(stkList, context):
	# 去除创业板股票
	if context.isFilterGem:
		return [stk for stk in stkList if not stk[:3] == '300']
	else:
		return stkList


def filterStAndPaused(stkList):
	stkList = [stk for stk in stkList if not is_st_stock(stk) and not is_st_stock(stk)]
	return stkList


def filterLimitStk(stk, bar_dict, context):
	# 去除上市小于三十天的新股
	
	# '''可能会有问题'''
	yesterday = history_bars(stk, 2, '1d', 'close')[-1]
	his = history_bars(stk, 2, '1d', 'close')[-1]
	zt = round(1.10 * yesterday, 2)
	dt = round(0.97 * yesterday, 2)
	if dt < bar_dict[stk].last < zt:
		return False
	else:
		return True


def filterNewStk(context, bar_dict, stk):
	listedDate = instruments(stk).listed_date.date()
	now = context.now.date()
	if (now - listedDate).days < 30:
		return True
	else:
		return False


def handle_bar(context, bar_dict):
	if True:  # context.flag % context.tradePeriod == 0:
		now = context.now
		if now.hour == 14 and now.minute == 40:
			if isSafe(bar_dict, context):
				stkList = filterGem(context.stocks1, context)
				stkList = filterStAndPaused(stkList)
				stkList = [stk for stk in stkList if
				           not filterNewStk(context, bar_dict, stk) and not filterLimitStk(stk, bar_dict, context)]
				stkList = [stk for stk in stkList if not is_st_stock(stk) and not is_suspended(stk)]
				stkList = [stk for stk in stkList if stk not in context.blackList]
				stkList = stkList[:20]
				stkList = getScore(stkList, bar_dict, context)
				stkList = stkList[:context.holdSize]
				print(stkList)
				weight = context.portfolio.portfolio_value * context.holdWeight
				context.tgtOrder = {}
				context.isBuy = {}
				for stk in stkList:
					context.tgtOrder[stk] = weight
					context.isBuy[stk] = True
			else:
				context.isBuy = {}
				context.tgtOrder = {}
				weight = context.portfolio.portfolio_value * 0.099
				for stk in context.stocks2:
					context.tgtOrder[stk] = weight
					context.isBuy[stk] = True
		tgtOrder = context.tgtOrder
		# if now.year == 2015 and now.month==6 and now.day>=20 and now.hour==14 and now.minute ==40:
		#     stocks = ['601288.XSHG','000898.XSHE','601988.XSHG','601398.XSHG','600000.XSHG','600649.XSHG','601328.XSHG','600019.XSHG','601166.XSHG','601939.XSHG']
		#     weight = context.portfolio.portfolio_value*0.099
		#     tgtOrder = {}
		#     for stk in stocks:
		#         tgtOrder[stk] = weight
		
		# if now.year == 2015 and now.month==6 and now.day>=20 and now.hour==14 and now.minute ==40:
		#     stocks = ['601288.XSHG','000898.XSHE','601988.XSHG','601398.XSHG','600000.XSHG','600649.XSHG','601328.XSHG','600019.XSHG','601166.XSHG','601939.XSHG']
		#     weight = context.portfolio.portfolio_value*0.099
		#     tgtOrder = {}
		#     for stk in stocks:
		#         tgtOrder[stk] = weight
		
		# if not isSafe(bar_dict) and now.hour==14 and now.minute ==40 :
		#     tgtOrder = {}
		#     weight = context.portfolio.portfolio_value*0.099
		#     for stk in context.stocks2 :
		#         tgtOrder[stk]=weight
		
		if now.hour == 14 and now.minute >= 41:
			weight = context.portfolio.portfolio_value * context.holdWeight
			email_info = ""
			for stk in context.portfolio.positions.keys():
				if stk not in tgtOrder.keys():
					order1 = order_target_percent(stk, 0)
					# email and persist
					if order1.status == ORDER_STATUS.FILLED:
						info1 = insert_2_text(context.logFileName, order1)
						email_info += info1
				if context.portfolio.positions[stk].market_value > weight:
					order1 = order_target_value(stk, weight * 0.99)
					# email and persist
					if order1.status == ORDER_STATUS.FILLED:
						info1 = insert_2_text(context.logFileName, order1)
						email_info += info1
			emailsender(context.receivers, email_info, 'stock_order_info')
		
		if now.hour == 14 and now.minute >= 45:
			email_info = ""
			for stk in tgtOrder.keys():
				if context.portfolio.positions[stk].market_value > tgtOrder[stk] * 0.97:
					context.isBuy[stk] = False
				if stk not in context.portfolio.positions.keys():
					order1 = order_target_value(stk, tgtOrder[stk])
					# email and persist
					if order1.status == ORDER_STATUS.FILLED:
						info1 = insert_2_text(context.logFileName, order1)
						email_info += info1
				if stk in context.portfolio.positions.keys() and context.portfolio.positions[stk].market_value < \
								tgtOrder[stk] * 0.98 and context.isBuy[stk]:
					order1 = order_target_value(stk, tgtOrder[stk])
					# email and persist
					if order1.status == ORDER_STATUS.FILLED:
						info1 = insert_2_text(context.logFileName, order1)
						email_info += info1
			emailsender(context.receivers, email_info, 'stock_order_info')

