#!/usr/bin/env python
#-*- coding:utf8 -*-

'''
copyright @wangxiaojie 2020.03.19
author: wangxiaojie
'''

import os, sys

codePath = os.path.abspath(os.path.join(__file__, "..", "Code"))
if os.path.exists(codePath):
    sys.path.append(codePath)
from EmailController import *

if __name__ == "__main__":
    emailController = EmailController() #实例化一个EmailController
    confFile = os.path.abspath(os.path.join(__file__, "../etc/email.json"))
    result = emailController.initWithConfigFile(confFile) #使用配置文件初始化
    ret = emailController.sendEmailWithTag("test", "测试邮件", "这是一份测试邮件")
    