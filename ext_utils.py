#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

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
	info = order.datetime.strftime("%Y-%m-%d %H:%M:%S") + ' ' + str(order.order_book_id) + ' ' \
		+ str(order.side) + ' ' + str(order.quantity)
	fp.writelines(info+'\n')
	
	
	