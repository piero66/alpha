#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from rqalpha.environment import Environment
from rqalpha.mod.rqalpha_mod_sys_stock_realtime.utils import get_tick, get_realtime_quotes, order_book_id_2_tushare_code

# receivers：接受邮件邮箱
# all_text：文件内容
# event_subject：邮箱标题
def emailsender(receivers, all_text, event_subject):
	# 第三方 SMTP 服务
	mail_host = "smtpdm.aliyun.com"  # 设置服务器
	mail_user = "tb@mail.wokens.com"  # 用户名
	mail_pass = "wokens6666"  # 口令

	sender = 'tb@mail.wokens.com'

	message = MIMEText(all_text, 'plain', 'utf-8')  # 邮件内容
	message['From'] = Header(sender, 'utf-8')  # 发件人


	message['Subject'] = Header(event_subject, 'utf-8')#标题

	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mail_host, 25)
		smtpObj.login(mail_user, mail_pass)
		for receiver in receivers:
			message['To'] = Header(receiver, 'utf-8')  # 收件人
			smtpObj.sendmail(sender, receiver, message.as_string())
		print("邮件发送成功")
	except smtplib.SMTPException:
		print("Error: 无法发送邮件")


def insert_2_text(filename, order):
	fp = open(filename, 'a')
	info = order.datetime.strftime("%Y-%m-%d %H:%M:%S") + '  ' + str(order.order_book_id) + '  ' \
		+ str(order.side) + '  ' + str(order.quantity) + '  ' + str(order.price) + '\n'
	fp.writelines(info)
	return info


def get_fundamental(search_value):
	order_book_id_list = sorted(Environment.get_instance().data_proxy.all_instruments("CS").order_book_id.tolist())
	code_list = [order_book_id_2_tushare_code(code) for code in order_book_id_list]
	realtime_tick = get_tick(code_list, 'qq')
	v_list = realtime_tick
	
	# 筛选
	if search_value['maxMarket_cap']:
		v_list = {k: v for k, v in v_list.items() if v['total_market_value'] < search_value['maxMarket_cap']}
	if search_value['minMarket_cap']:
		v_list = {k: v for k, v in v_list.items() if v['total_market_value'] > search_value['minMarket_cap']}
	if search_value['maxPE']:
		v_list = {k: v for k, v in v_list.items() if v['PE'] is not None and v['PE'] < search_value['maxPE']}
	if search_value['minPE']:
		v_list = {k: v for k, v in v_list.items() if v['PE'] is not None and v['PE'] > search_value['minPE']}
	if search_value['maxPB']:
		v_list = {k: v for k, v in v_list.items() if v['PB'] is not None and v['PB'] < search_value['maxPB']}
	if search_value['minPB']:
		v_list = {k: v for k, v in v_list.items() if v['PB'] is not None and v['PB'] > search_value['minPB']}
		
	v_list = {k: v for k, v in v_list.items() if v['close'] > 0}  # 去除退市
	
	# 排序
	t_list = {}
	for code, data in v_list.items():
		t_list[code] = data[search_value['sort']]
	f_list = sorted(t_list.items(), key=lambda x: x[1], reverse=False)
	t_list = []
	for (k, v) in f_list:
		t_list.append(k)
	return t_list



'''
value_d = {}
for code, data in realtime_tick.items():
	value_d[code] = data[search_value] # 'total_market_value'
list1 = sorted(value_d.items(), key=lambda value_d: value_d[1], reverse=False)
realtime_quotes_df = get_realtime_quotes(code_list)

['002133.XSHE', '600766.XSHG', '000668.XSHE', '000880.XSHE', '600145.XSHG']
['300029.XSHE', '300321.XSHE', '000995.XSHE', '600768.XSHG', '600385.XSHG']
'''
	
	