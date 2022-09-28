#!/usr/bin/python
# -*- coding: UTF-8 -*-
import base64
import configparser
import ctypes
import os

from win32com.client import Dispatch


def getDM():
    try:
        dmObject = Dispatch('dm.dmsoft')
        print('本机系统中已经安装大漠插件，版本为:', dmObject.ver())
    except:
        print('本机并未安装大漠，正在免注册调用')
        dms = ctypes.windll.LoadLibrary(os.getcwd() + r'\DmReg.dll')
        location_dmreg = os.getcwd() + r'\dm.dll'
        dms.SetDllPathW(location_dmreg, 0)
        dmObject = Dispatch(r'dm.dmsoft')
        print('免注册调用成功 版本号为:', dmObject.Ver())
        return dmObject


def DmInit():
    cf = configparser.ConfigParser()
    cf.read("./data.ini")
    param1 = cf.get("password", "param1")
    param2 = cf.get("password", "param2")
    param1 = base64.b64decode(param1)
    param2 = base64.b64decode(param2)
    dm = getDM()
    dm.SetPath(os.getcwd())
    res = dm.Reg(param1, param2)
    if res == 1:
        print("大漠插件注册成功")