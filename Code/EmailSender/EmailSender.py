#!/usr/bin/env python
#-*- coding: UTF-8 -*- 

'''
copyright @wangxiaojie 2020.02.19
author: wangxiaojie
'''

import os, sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

__all__ = [
    "sendEmail",
    "emailLogger"
    ]

emailLogger = logging.Logger("EmailSender")
    
def sendEmail(email_host, email_sender, email_auth, receive_list, to_str, subject, content, attach_dict):
    #email_host = 'smtp.qq.com'        # 邮箱服务器地址
    #email_user = '********@qq.com'  # 发送者账号
    #email_pwd = '*********'    # 发送者的授权码
    #maillist =['********@qq.com']   # 接受者列表，收件人邮箱，多个账号的话，用逗号隔开 
    #to_str = '**<***********@qq.com>, **<***********@qq.com>'  #接受者显示文字
    #subject 邮件主题
    #邮件内容
    #邮件附件
      
    try:
        msg = MIMEMultipart()    
        msg.attach(MIMEText(content)  )  # 邮件内容
        msg['Subject'] = subject    # 邮件主题
        msg['From'] = email_sender    # 发送者账号
        msg['To'] = to_str    
        if attach_dict:
            for key in attach_dict:
                if os.path.isfile(key):
                    temp_attach = MIMEText(open(key, 'rb').read(), 'base64', 'utf-8')
                    temp_attach['Content-Type'] = 'application/octet-stream'
                    temp_attach['Content-Disposition'] = "attachment; filename = \"%s\"" % attach_dict[key]
                    msg.attach(temp_attach)
        smtp = smtplib.SMTP(email_host) # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
        smtp.login(email_sender, email_auth)   # 发送者的邮箱账号，密码
        smtp.sendmail(email_sender, receive_list, msg.as_string())
        # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
        smtp.quit() # 发送完毕后退出smtp
        emailLogger.debug('email send success.')
    except Exception as e: 
        emailLogger.error("email send error: ", e)
        return False
    return True
        
if __name__ == "__main__":
    attach1 = os.path.abspath(os.path.join(__file__, "../../README.md"))
    result = sendEmail('smtp.qq.com', '***@qq.com', '***', ['***@qq.com', '***@qq.com'], '**<***@qq.com>, **<***@qq.com>', "测试邮件", "这是一封测试邮件", {attach1: "log1"})
    if result:
        print("success")
    else:
        print("failed")