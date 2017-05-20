alpha 基于rqalpha做的一些功能改进，添加自己需要的功能。

现在基于原realtime_stock mod，支持获取esayquotation实时数据，也包括原来包含的tushare实时数据，
实时更新来源rqalpha的本地历史数据。
通过esayquotation 获取了财务信息，包括市值,PE,PB 筛选股票

一.程序运行方式
1.terminal 直接执行 python Run.py
  策略参数选项
  config = {
    "base": {
        "run_id": "0031",
        "strategy_file": "strategy_t.py",  #  策略名称： strategy_t.py
        "strategy_type": "stock",          #  策略类型：  股票
        "stock_starting_cash": 10000000,   #  模拟策略初始资金：  10000000
        "run_type": "p",                   #  运行方式： 实盘模拟
        "frequency": "1m",
        "data_bundle_path": ".rqalpha/bundle/"  #  历史数据存储路径： .rqalpha/bundle/
    },
    "extra": {
        "log_level": "verbose",            #  日志级别：  全部日志
    },
    "mod": {
        "sys_stock_realtime": {
        "enabled": True,
        }
    },
}


二.策略函数相关
1.history_bars 使用，该函数可以获取某只股票的即使数据
函数原型：history_bars(order_book_id, bar_count, frequency, fields=None, skip_suspended=True, include_now=False)

实时数据用法：history_bars('601988.XSHG', 1, '1m', 'tick') 即第一个参数是股票代码，第四个参数是'tick'
实时数据格式：
{'601988.XSHG': {
'order_book_id': '601988.XSHG',
'open': 3.62,
'close': 3.62,
'last': 3.62,
'high': 3.63,
'low': 3.6,
'bid': [3.61, 3.6, 3.59, 3.58, 3.57],                #卖一到卖五
'bid_volume': [3403079, 16759322, 3129900, 2934300, 1006600],
'ask': [3.62, 3.63, 3.64, 3.65, 3.66],               #买一到买五
'ask_volume': [10019420, 18951311, 9160700, 9359300, 3100580],
'datetime': datetime.datetime(2017, 4, 11, 15, 0),
'open_interest': nan,
'limit_up': nan,
'limit_down': nan,
'prev_close': 3.63,
'total_turnover': 147514101,
'volume': 533087041.0,
'prev_settlement': nan
}
}

2.当前仓位信息
context.portfolio
context.portfolio.positions['股票代码']

3.股票财务数据
get_fundamental(search_value)
search_value = {
			'maxMarket_cap': 50,   #  市值的范围 最大值
			'minMarket_cap': 0,    #            最小值
			'maxPE': None,         #  PE的范围   最大值
			'minPE': 0,            #            最小值
			'maxPB': None,         #  PB的范围   最大值
			'minPB': None,         #            最小值
			'sort': 'total_market_value',       #根据总市值排序
		}

4.使用bar_dict获取实时数据 来源TuShare.