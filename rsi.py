from rqalpha.api import *
import talib

from ext_utils import *


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):

    # 选择股票
    context.s1 = "600104.XSHG"
    context.s2 = "000895.XSHE"
    
    # 交易信号
    context.orderFlag1 = True
    context.orderFlag2 = True
    # 交易信息保存文件
    context.logFileName = 'log_info.txt'
    
    # 接收邮箱
    context.receivers = ['623486086@qq.com']
    
# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑
    
    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息
    
    # 查询持仓
    print(context.portfolio.positions[context.s1])
    print(context.portfolio.positions[context.s2])
    
    # 使用history_bars(book_order_id, mount, frequency, 'tick')方法进行数据获取
    
    price1 = history_bars(context.s1, 1, '1m', 'tick')
    price2 = history_bars(context.s2, 1, '1m', 'tick')
    volume1 = price1['bid_volume'][0]
    volume2 = price2['ask_volume'][0]
    # wait to fix 下单失败后 尚未处理
    # 策略逻辑
    if price1['bid'][0] - price2['ask'][0] > 4.1:
        if context.orderFlag1:
            order1 = order_lots(context.s1, 1)
            order2 = order_lots(context.s2, 1)
            if order1.status == ORDER_STATUS.FILLED and order2.status == ORDER_STATUS.FILLED:
                info1 = insert_2_text(context.logFileName, order1)  # order信息 保存到本地
                info2 = insert_2_text(context.logFileName, order2)  # order信息 保存到本地
                context.orderFlag1 = False
                all_text = info1 + '\n' + info2
                emailsender(context.receivers, all_text, 'stock_order')
            else:
                context.orderFlag1 = True
        
    else:
        context.orderFlag1 = True
        
    if price1['ask'][0] - price2['bid'][0] < 3.5:
        if context.orderFlag2:
            order1 = order_lots(context.s1, 1)
            order2 = order_lots(context.s2, -1)
            if order1.status == ORDER_STATUS.FILLED and order2.status == ORDER_STATUS.FILLED:
                info1 = insert_2_text(context.logFileName, order1)  # order信息 保存到本地
                info2 = insert_2_text(context.logFileName, order2)  # order信息 保存到本地
                context.orderFlag2 = False
                all_text = info1 + '\n' + info2
                emailsender(context.receivers, all_text, 'stock_order')
            else:
                context.orderFlag2 = True
    else:
        context.orderFlag2 = True

