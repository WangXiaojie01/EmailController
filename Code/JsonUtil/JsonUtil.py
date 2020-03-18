#!/usr/bin/env python
#-*- coding:utf8 -*-

'''
copyright @wangxiaojie 2020.01.18
author: wangxiaojie
'''

import os,sys
import json
import traceback
import logging

__all__ = [
    "getJsonFromFile",
    "getJsonFromStr",
    "valueFromJsonFile",
    "valueFromJsonStr",
    "saveJsonFile",
    "getDefaultFromJsonObj",
    "combineUnitList",
    "jsonLogger"
    ]

jsonLogger = logging.Logger("JsonUtil")

def getJsonFromFile(filename):
    try:
        fp = open(filename)
        if fp == None:
            return None
        jobject = json.load(fp)
        fp.close()
        return True, jobject 
    except Exception as e:
        jsonLogger.error("exception is %s" % e)
        return False, "%s"%e

def getJsonFromStr(jsonstr):
    try:
        jobject = json.loads(jsonstr)
        return True, jobject
    except Exception as e:
        jsonLogger.error("exception is %s" % e)
        return False, "%s"%e

def valueFromJsonFile(key, filename):
    if not os.path.isfile(filename):
        return False
    result, jsonParams = getJsonFromFile(filename)
    if not result:
        return False
    if key in jsonParams:
        return jsonParams[key]
    return False

def valueFromJsonStr(key, jsonStr):
    result, jsonParams = getJsonFromStr(jsonStr)
    if not result:
        return False
    if key in jsonParams:
        return jsonParams[key]
    return False
    
def saveJsonFile(filepath, data):
    try:
        finalStr = json.dumps(data, indent=4, ensure_ascii=False).encode("utf8")
        fp = open(filepath, 'bw')
        params = fp.write(finalStr)
        fp.close()
        return True, "success"
    except Exception as e:
        return False, "%s"%e

def getDefaultFromJsonObj(key, jsonObj):
    if key and jsonObj:
        if isinstance(jsonObj, dict):
            if key in jsonObj:
                return jsonObj[key], 'success'
            elif 'default' in jsonObj:
                return jsonObj['default'], 'success'
            else:
                errorStr = '%s is not found in jsonObj' % key
                jsonLogger.error(errorStr)
                return None, errorStr
        else:
            return jsonObj, 'success'
    else:
        jsonLogger.error('key or jsonObj is None')
        return None, 'key or jsonObj is None'

def combineUnitList(list1, list2):
    newList =[]
    if list1:
        for item in list1:
            if not item in newList:
                newList.append(item)
    if list2:
        for item in list2:
            if not item in newList:
                newList.append(item)
    return newList

