# -*-coding:utf-8 -*-
import base64
import configparser

import win32gui
from PyGameAutoFree import *

cf = configparser.ConfigParser()
cf.read("./data.ini")
param1 = cf.get("password", "param1")
param2 = cf.get("password", "param2")
param1 = base64.b64decode(param1)
param2 = base64.b64decode(param2)
dm = PyGameAuto.gl_init(param1, param2)
path = PyGameAuto.get_path(__file__)
# 句柄
hwnd = win32gui.FindWindow(None,
                           u"剑网贰单机版(交流QQ群:985964773)-此客户端与服务端免费分享 (公益怀旧群服专用客户端)")
while hwnd <= 0:
    # 打开游戏
    dm.RunApp(r"D:\games\剑网贰怀旧群服客户端\so2game.exe", 1)
    sleep(10)
    hwnd = win32gui.FindWindow(None,
                               u"剑网贰单机版(交流QQ群:985964773)-此客户端与服务端免费分享 (公益怀旧群服专用客户端)")
ret = dm.BindWindow(hwnd, "dx", "dx", "dx", 1)
dm.MoveWindow(hwnd, -16, -26)
dm.SetWindowSize(hwnd, 1024, 768)
dm.SetDict(0, "new.txt")
h, x, y = dm.FindStrFast(385, 611, 547, 665, "开始游戏", "#255-9b9b9b", 0.8)
h, x, y = int(h), int(x), int(y)
if x >= 0 and y >= 0:
    dm.