# -*-coding:utf-8 -*-
import base64
import configparser
import time

from PyGameAutoFree import *

cf = configparser.ConfigParser()
cf.read("./data.ini")
param1 = cf.get("password", "param1")
param2 = cf.get("password", "param2")
param1 = base64.b64decode(param1)
param2 = base64.b64decode(param2)
dm = PyGameAuto.gl_init(param1, param2)
path = PyGameAuto.get_path(__file__)
dm.SetDict(0, "dic.txt")
stat = 'init'


def init():
    # 判断是否在首页
    h, x, y = dm.FindPic(0,0,1025,1027, "首页文字标题.bmp", 0.8)
    if x < 0 and y < 0:
        print('不在首页，需要转到首页')
        # 点击首页
        h, x, y = dm.FindPic(0,0,1025,1027, "首页按钮.bmp", 0.8)
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            dm.LeftClick()
            print("识别到首页按钮")


def 开枪():
    hasItem = True
    searchTime = 0
    while hasItem:
        # 点击盒子
        h, x, y = dm.FindPic(0,0,1025,1027, "需要抢的盒子.bmp", 0.8)
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            dm.LeftClick()
        else:
            searchTime += 1
            if searchTime >= 20:
                break
        h, x, y = dm.FindPic(0,0,1025,1027, "确认按钮.bmp", 0.8)
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            dm.LeftClick()
        dm.WheelDown()
        dm.WheelDown()


def fetch():
    点击竞拍已开始()
    开枪()


def 点击竞拍已开始():
    # 点击开始竞拍按钮
    isFind = False
    while not isFind:
        h, x, y = dm.FindPic(0,0,1025,1027, "竞拍已开始.bmp", 0.8)
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            dm.LeftClick()
            isFind = True


def runTask():
    global stat
    while not stat.__eq__("stop"):
        if stat.__eq__("init"):
            init()
            stat = 'waiting'
            print('初始化已完成，现在等待7：00开枪')
            continue
        if stat.__eq__("waiting"):
            init()
            nowStr = getNowTimeStr()
            now = int(nowStr)
            if now >= 144100:
                print('还有十分钟开枪')
                stat = 'fetch'
            else:
                print("当前没在抢票时间：现在时间是" + nowStr)
            continue
        if stat.__eq__("fetch"):
            fetch()
            print('已完成')
            stat = 'end'
            continue
        if stat.__eq__('end'):
            break


def getNowTimeStr():
    return time.strftime('%H%M%S', time.localtime())


if __name__ == '__main__':
    runTask()
    # init()
