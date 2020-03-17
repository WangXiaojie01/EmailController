#!/usr/bin/env python
#-*- coding:utf8 -*-

'''
copyright @wangxiaojie 2020.03.16
author: wangxiaojie
'''

import os,sys
import logging

__all__ = [
    "readFile",
    "fileLogger"
    ]

fileLogger = logging.Logger("FileUtil")

def readFile(fileName):
    if fileName == None or not os.path.isfile(fileName):
        fileLogger.warning("%s is None or is not a file" % fileName)
        return None
    try:
        fopen = open(fileName, 'r')
        content = fopen.read()
        return content
    except Exception as e:
        fileLogger.error("readFile %s error, error msg is %s" % (fileName, e))
        return ""