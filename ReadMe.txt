一.程序运行方式
1.terminal 执行 python Run.py
2.PyCharm运行Run.py

二.策略函数相关
1.history_bars 使用
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
'bid': [3.61, 3.6, 3.59, 3.58, 3.57],
'bid_volume': [3403079, 16759322, 3129900, 2934300, 1006600],
'ask': [3.62, 3.63, 3.64, 3.65, 3.66],
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