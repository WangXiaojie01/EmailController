#!/usr/bin/env python
#-*- coding: UTF-8 -*- 

'''
copyright @wangxiaojie 2020.03/12
author: wangxiaojie
'''

import os, sys

emailSenderDir = os.path.abspath(os.path.join(__file__, "..", "EmailSender"))
if os.path.exists(emailSenderDir):
    sys.path.append(emailSenderDir)
JsonUtilDir = os.path.abspath(os.path.join(__file__, "..", "JsonUtil"))
if os.path.exists(JsonUtilDir):
    sys.path.append(JsonUtilDir)

from EmailSender import *
from JsonUtil import *

__all__ = [
    "EmailController"
    ]

class EmailController(object):
    def __init__(self):
        self.emailHostList = None
        self.emailSendersList = None
        self.emailReceiversList = None 
        self.nameEmialMapList = None
        self.emailHost = None 
        self.emailSenders = None 
        self.emailSender = None 
        self.emailAuth = None 
        self.emailReceivers = None 
        self.emailToStr = None 
        self.emailAttachDict = None 
        self.emailSubject = None 
        self.emailContent = None 
        self.nameEmailMap = None
        self.hasInit = False
        self.emailConfFile = None

    def __init__(self, emailHost, emailSender, emailAuth, emailReceivers, toStr):
        self.emailHost = emailHost
        self.emailSender = emailSender
        self.emailAuth = emailAuth
        self.emailReceivers = emailReceivers
        self.emailToStr = toStr
        self.hasInit = True

    def __init__(self, configFile):
        if not os.path.isfile(configFile):
            emailLogger.error('%s is not a file' % configFile)
            return False
        result, emailJsonDict = getJsonFromFile(configFile)
        if result:
            if "email_hosts" in emailJsonDict:
                self.emailHost = emailJsonDict["email_hosts"]
            if "email_senders" in emailJsonDict:
                self.emailSendersList = emailJsonDict["email_senders"]
            if "email_receivers" in emailJsonDict:
                self.emailReceiversList = emailJsonDict["email_receivers"]
            if "name_email_map" in emailJsonDict:
                self.nameEmialMapList = emailJsonDict["name_email_map"]
            self.hasInit = True
            self.emailConfFile = configFile
            return True
        else:
            emailLogger.error('getJsonFromFile(%s) error' % configFile)
            return False

    def sendEmail(self):
        result = sendEmail(self.emailHost, self.emailSender, self.emailAuth, self.emailReceivers, self.emailToStr, self.emailSubject, self.emailContent, self.emailAttachDict)
        if not result:
            emailLogger.error("sendEmail Error")
            return False
        return True

    def sendEmailWithTag(self, tag, subject, content, otherReceivers = None, attach = None):
        if self.hasInit:
            if self.emailHostList == None or \
                self.emailSendersList == None or \
                self.emailReceiversList == None
                emailLogger.error('email_hosts or email_senders or email_receivers is None in %s' % self.emailConfFile)
                return False
            self.emailHost, result = getDefaultFromJsonObj(tag, self.emailHostList)
            if result != "success": 
                emailLogger.error("get %s from email_hosts failed" % tag)
                return False
            if self.emailHost == None or len(self.emailHost) == 0:
                emailLogger.error("%s in email_hosts is None or empty" % tag)
                return False 
            self.emailSenders, result = getDefaultFromJsonObj(tag, self.emailSendersList)
            if result != "success": 
                emailLogger.error("get %s from email_senders failed" % tag)
                return False
             if self.emailSenders == None or len(self.emailSenders) == 0:
                emailLogger.error("%s in email_senders is None or empty" % tag)
                return False 
            self.emailReceivers, result = getDefaultFromJsonObj(tag, self.emailReceiversList)
            if result != "success": 
                emailLogger.error("get %s from email_receivers failed" % tag)
                return False
            if (self.emailReceivers == None or len(self.emailReceivers) == 0) \
                and (otherReceivers == None or len(otherReceivers) == 0):
                emailLogger.error("both %s in email_receivers and otherReceivers is None or empty")
                return False
            if self.nameEmialMapList != None and len(self.nameEmialMapList) > 0:
                self.nameEmailMap, result = getDefaultFromJsonObj(tag, self.nameEmialMapList)
            self.combineEmailReceivers(otherReceive)
            if self.emailReceivers == None or len(self.emailReceivers) == 0:
                emailLogger.error("noting in receivers after combineEmailReceivers")
                return False
            self.getEmailToStr()
            self.emailSubject = subject
            self.emailContent = content
            self.emailAttachDict = attach
            sendResult = False
            for sender, auth in self.emailSenders:
                self.emailSender = sender
                self.emailAuth = auth
                if self.sendEmail():
                    sendResult = True
                    break
                else:
                    emailLogger.error("%s send email error" % sender)
            return sendResult
        else:
            emailLogger.error("EmailController has not inited")
            return False

    def combineEmailReceivers(self, otherReceivers):
        receivers1 = analyzeReceiverStr(self.emailReceivers)
        receivers2 = analyzeReceiverStr(otherReceivers)
        self.emailReceivers = combineUnitList(receivers1, receivers2)
        
    def analyzeReceiverStr(self, receivers):
        if isinstance(receivers, str):
            newReceivers = receivers.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "")
            while ",," in newReceivers:
                newReceivers = newReceivers.replace(",,", ",")
            receivers = newReceivers.split(",")
        if isinstance(receivers, list):
            newRecievers = []
            for i, val in enumerate(receivers):
                if val in self.nameEmailMap:
                    newReceivers.append(self.nameEmailMap[val])
                else:
                    if val.find("@") >= 0:
                        newReceivers.append(val)
            return newReceivers
        return None

    def getEmailToStr(self):
        newStr = ""
        for i, val in enumerate(self.emailReceivers):
            tempStr = "%s<%s>" % (val, val)
            for key, value in self.nameEmailMap:
                if val == value:
                    tempStr = "%s<%s>" % (key, value)
                    break
            if newStr == "":
                newStr = tempStr
            else:
                newStr = "%s;%s" % (newStr, tempStr)
        self.emailToStr = newStr
    
    def sendWithTagAndFile(self, tag, subject, contentFile, contentHeader = None, contentTail = None, otherReceivers = None, attach = None):
        if contentFile == None:
            emailLogger.error("contentFile must be assigned with a file")
            return False
        emailContent = "%s\n%s\%s" % (self.readFile(contentHeader), self.readFile(contentFile), self.readFile(contentTail))
        return self.sendEmailWithTag(tag, subject, emailContent, otherReceivers, attach)

    def readFile(self, fileName):
        if fileName == None or not os.path.isfile(fileName):
            return ""
        try:
            fopen = open(fileName, 'r')
            content = fopen.read()
            return content
        except Exception as e:
            return ""

if __name__ == "__main__":
    email_json = os.path.abspath(os.path.join(__file__, "../../etc/email/email.json"))
    if os.path.exists(email_json):
        print "exist"

    email_sender = EmailController(email_json)

    attach_path = os.path.abspath(os.path.join(__file__, "../../etc"))
    email_attach = {os.path.join(attach_path, "README.md"): "test_attach"} #, os.path.join(attach_path, "project/other/monitor.json"): "附件2"}
    #email_attach = [os.path.join(attach_path, "email_tail.conf"), os.path.join(attach_path, "project/other/monitor.json")]
    print "is %s"%email_json
    
    email_sender.sendEmailWithService("test", "测试邮件", "这是一封测试邮件，如果你收到了，恭喜你，中奖了", None, email_attach, True)
   