# -*-coding:utf-8 -*-
import base64
import configparser
import hashlib
import random
import time
from tkinter import *
from tkinter import messagebox

import win32gui
from PyGameAutoFree import *
from init import *
from item import items
from enemys import enemyList
from tpms import tpms

cf = configparser.ConfigParser()
cf.read("./data.ini")
param1 = cf.get("password", "param1")
param2 = cf.get("password", "param2")
param1 = base64.b64decode(param1)
param2 = base64.b64decode(param2)
dm = PyGameAuto.gl_init(param1, param2)
path = PyGameAuto.get_path(__file__)
equipmentToBePickedUp = ["五色玉佩", "墨玉玉佩", "琥珀护身符", "红翡翠护身符", "蓝水晶戒指", "钻石戒指"]
# 句柄
hwnd = win32gui.FindWindow(None,
                           u"剑网贰单机版(交流QQ群:985964773)-此客户端与服务端免费分享 (公益怀旧群服专用客户端)")
while hwnd <= 0:
    print('未发现游a戏窗口，请打开')
hwnd = win32gui.FindWindow(None,
                           u"剑网贰单机版(交流QQ群:985964773)-此客户端与服务端免费分享 (公益怀旧群服专用客户端)")
time.sleep(1)
dm_ret = dm.BindWindowEx(hwnd, "dx2",
                         "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.focus.input.api|dx.mouse.focus.input.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.state.message|dx.mouse.api|dx.mouse.cursor|dx.mouse.raw.input|dx.mouse.input.lock.api2|dx.mouse.input.lock.api3",
                         "windows", "", 0)
dm.MoveWindow(hwnd, 0, 0)
dm.SetWindowSize(hwnd, 1030, 738)
dm.SetDict(0, "new.txt")
enemyNames = ["异族箭手", "异族武士", "精英异族箭手", "精英异族武士", "辽刀兵", "辽枪兵", "精英辽刀兵", "精英辽枪兵"]
enemyX, enemyY, enemyT = None, None, None
hero = {
    'x': 517,
    'y': 398
}


def state():
    dm.MoveTo(hero.get('x'), hero.get('y'))
    dm.LeftClick()
    plusState(65)  # a
    time.sleep(1)
    plusState(68)  # d
    time.sleep(1)
    plusState(81)  # q
    time.sleep(1)
    plusState(83)  # s
    time.sleep(1)
    plusState(87)  # w
    print("已加完state")


def plusState(key):
    dm.KeyPress(key)
    dm.MoveTo(hero.get('x'), hero.get('y'))
    dm.RightClick()
    time.sleep(1)
    print("plusState" + str(key))


def findTheNearestMonster():
    for i in enemyNames:
        s = enemyList[i]
        h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        h, x, y = toInt(h, x, y)
        if x >= 0 and y >= 0:
            return True, x, y, s[4]
    return False, -1, -1, None


def toInt(h1, x1, y1):
    return int(h1), int(x1), int(y1)


def findTheMonsterOnTheScreen():
    for i in enemyNames:
        s = enemyList[i]
        h, x, y = dm.FindStrFast(0, 0, 1018, 670, s[4], s[5], s[6])
        h, x, y = toInt(h, x, y)
        if x >= 0 and y >= 0:
            return True, x, y, s[4]
    return False, -1, -1, None


def findTheMonsterNearTheSmallMap():
    pic = tpms["怪小地图"]
    h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
    if x >= 0 and y >= 0:
        print("找到了：" + pic[4] + "地址：（" + str(x) + "," + str(y) + "）")
        return True, x, y, pic[4]
    else:
        return False, -1, -1, None


def walk(di, step, t):
    print(di, step, t)
    if di.__eq__("L"):
        # 尝试左走
        dm.MoveTo(hero.get('x') - 100 * step, hero.get('y'))
    elif di.__eq__("R"):
        # 尝试右走
        dm.MoveTo(hero.get('x') + 100 * step, hero.get('y'))
    elif di.__eq__("U"):
        # 尝试上走
        dm.MoveTo(hero.get('x'), hero.get('y') - 70 * step)
    elif di.__eq__("D"):
        # 尝试上走
        dm.MoveTo(hero.get('x'), hero.get('y') + 70 * step)
    for i in range(t):
        dm.LeftClick()
        time.sleep(0.5)


def rambleAbout():
    dis = ['L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'U', 'D']
    # 随机一个方向和step
    dindex = random.randint(0, 9)
    print("dindex=" + str(dindex))
    step = random.randint(1, 3)
    times = random.randint(1, 8)
    walk(dis[dindex], step, times)
    time.sleep(2)


def findTheWildMonster():
    isFind = False
    while not isFind:
        isFind, dx, dy, eType = findTheNearestMonster()
        if isFind:
            return dx, dy, eType
        else:
            isFind, dx, dy, eType = findTheMonsterOnTheScreen()
            if isFind:
                return dx, dy, eType
            else:
                isFind, dx, dy, eType = findTheMonsterNearTheSmallMap()
                if isFind:
                    dm.MoveTo(dx + 1, dy + 1)
                    dm.LeftClick()
                    time.sleep(3)
                    isFind = False
                else:
                    rambleAbout()
                    time.sleep(2)


numberClicks = {}


def strikeAMonster(ex, ey):
    key = str(ex) + "," + str(ey)
    if key in numberClicks.keys():
        if numberClicks[key] > 3:
            return
        else:
            numberClicks[key] += 1
    else:
        numberClicks[key] = 1
    dm.MoveTo(ex + 32, ey + 66)
    dm.LeftClick()
    print("已点击%s,%s", str(ex + 32), str(ey + 66))


def checkStatus():
    isFull = False
    # 查看背包是否满了
    pic = tpms["背包-空格子"]
    h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
    h, x, y = toInt(h, x, y)
    if x < 0 and y < 0:
        print("格子满了")
        isFull = True
    s = dm.Ocr(784, 604, 871, 630, "bdbebd-000000", 0.9)
    slist = str.split(s, "/")
    负重比 = int(slist[0]) / int(slist[1])
    print(负重比)
    if 负重比 > 0.9:
        isFull = True
        print("负重满了" + str(负重比))
    return isFull


def cleanBag():
    # 逐个查看没见装备的属性存入list中
    equipmentInfomations = []
    s = items["道具背包"]
    h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    h, x, y = toInt(h, x, y)
    if x < 0 or y < 0:
        dm.MoveTo(hero.get('x'), hero.get('y'))
        dm.LeftClick()
        dm.KeyPress(115)  # F4
        time.sleep(0.5)
    for i in range(5):
        for j in range(6):
            PointX, PointY = 788 + 21 + 42 * i, 347 + 21 + 42 * j
            dm.MoveTo(PointX, PointY)
            time.sleep(0.5)
            recognize = dm.Ocr(PointX - 762 + 573, 550, PointX - 762 + 732, 736,
                               "4a8eff-000000|ffb666-000000|ef4dbd-000000|5af363-000000|ffffff-000000|c6c3c6-000000",
                               0.9)
            print("坐标:" + str(PointX) + "," + str(PointY) + "---" + recognize)
            equipmentInfomations["eq" + str(i) + str(j)] = recognize
    s = items["扩展背包"]
    h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    h, x, y = toInt(h, x, y)
    if x < 0 or y < 0:
        pic = tpms["扩展背包按钮"]
        isFind = False
        while not isFind:
            h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
            h, x, y = toInt(h, x, y)
            if x >= 0 and y >= 0:
                dm.MoveTo(x, y)
                dm.LeftClick()
                isFind = True
    for i in range(5):
        for j in range(6):
            PointX, PointY = 573 + 21 + 42 * i, 350 + 21 + 42 * j
            dm.MoveTo(PointX, PointY)
            time.sleep(0.5)
            recognize = dm.Ocr(PointX - 762 + 573, 550, PointX - 762 + 732, 736,
                               "4a8eff-000000|ffb666-000000|ef4dbd-000000|5af363-000000|ffffff-000000|c6c3c6-000000",
                               0.9)
            print("坐标:" + str(PointX) + "," + str(PointY) + "---" + recognize)
            equipmentInfomations["eq" + str(i) + str(j)] = recognize


def doTask():
    time.sleep(2)
    print("辅助开始")
    stat = "初始化"
    x, y, etype = None, None, None
    while True:
        if stat.__eq__("初始化"):
            # plusState
            state()
            print("当前state：" + stat)
            stat = "找怪"
        elif stat.__eq__("找怪"):
            # 找怪
            print("findTheWildMonster中。。。")
            x, y, etype = findTheWildMonster()
            print("找到" + etype + ":(" + str(x) + "," + str(y) + ")")
            stat = "strikeAMonster"
        elif stat.__eq__("strikeAMonster"):
            # strikeAMonster
            strikeAMonster(x, y)
            print("strikeAMonster中。。。：")
            stat = "pickingUpEquipment"
        elif stat.__eq__("pickingUpEquipment"):
            # pickingUpEquipment
            pickingUpEquipment()
            print("当前state：" + stat)
            stat = "checkStatus"
        elif stat.__eq__("checkStatus"):
            # checkStatus
            # isBagFull = checkStatus()
            isBagFull = False
            print("当前state：" + stat)
            if isBagFull:
                stat = "cleanBag"
            else:
                stat = "找怪"
        elif stat.__eq__("cleanBag"):
            print("当前state：" + stat)
            cleanBag()
            stat = "找怪"


def pickingUpEquipment():
    for i in equipmentToBePickedUp:
        s = items[i]
        h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        h, x, y = toInt(h, x, y)
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            print("识别到：" + s[4] + ",坐标是:" + str(x) + "," + str(y))
            dm.LeftClick()
            time.sleep(2)
            openQualification()


def openQualification():
    unidentified_x, unidentified_y = findUnqualifiedEquipment()
    if unidentified_x >= 0 and unidentified_y >= 0:
        s = items["道具背包"]
        h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        h, x, y = toInt(h, x, y)
        if x < 0 or y < 0:
            dm.MoveTo(hero.get('x'), hero.get('y'))
            dm.LeftClick()
            dm.KeyPress(115)  # F4
            time.sleep(0.5)
        s = items["扩展背包"]
        h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        h, x, y = toInt(h, x, y)
        if x < 0 or y < 0:
            pic = tpms["扩展背包按钮"]
            isFind = False
            while not isFind:
                h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
                if x >= 0 and y >= 0:
                    dm.MoveTo(x, y)
                    dm.LeftClick()
                    isFind = True
        pic = tpms["七级鉴定符"]
        isFind = False
        while not isFind:
            h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
            h, x, y = toInt(h, x, y)
            if x >= 0 and y >= 0:
                dm.MoveTo(x, y)
                time.sleep(1)
                dm.RightClick()
                time.sleep(1)
                dm.MoveTo(315, 248)
                dm.MoveTo(unidentified_x, unidentified_y)
                dm.LeftClick()
                isFind = True
                # 识别这件装备的属性
                identifyEquipmentAttributes(unidentified_x)


def identifyEquipmentAttributes(x):
    # 573,550,732,736
    recognize = dm.Ocr(x - 762 + 573, 550, x - 762 + 732, 736,
                       "4a8eff-000000|ffb666-000000|ef4dbd-000000|5af363-000000|ffffff-000000|c6c3c6-000000", 0.9)
    print("识别的文字" + recognize)


def findUnqualifiedEquipment():
    unidentified_x, unidentified_y = -1, -1
    # 815,367,1017,613,宽高(202,246)
    s = items["道具背包"]
    h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    h, x, y = toInt(h, x, y)
    if x < 0 or y < 0:
        dm.MoveTo(hero.get('x'), hero.get('y'))
        dm.LeftClick()
        dm.KeyPress(115)  # F4
        time.sleep(0.5)
    for i in range(5):
        for j in range(6):
            PointX, PointY = 788 + 21 + 42 * i, 347 + 21 + 42 * j
            dm.MoveTo(PointX, PointY)
            s = items["未鉴定"]
            h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
            h, x, y = toInt(h, x, y)
            if x >= 0 and y >= 0:
                if j > 0:
                    unidentified_x, unidentified_y = 788 + 21 + 42 * i, 367 + 347 + 21 + 42 * (j - 1)
                else:
                    unidentified_x, unidentified_y = 788 + 21 + 42 * (i - 1), 367 + 347 + 21 + 40 * 5
                print("识别到：" + s[4] + ",坐标是:" + str(unidentified_x) + "," + str(unidentified_y))
                return unidentified_x, unidentified_y
            time.sleep(0.05)
    s = items["扩展背包"]
    h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    h, x, y = toInt(h, x, y)
    if x < 0 or y < 0:
        pic = tpms["扩展背包按钮"]
        isFind = False
        while not isFind:
            h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
            h, x, y = toInt(h, x, y)
            if x >= 0 and y >= 0:
                dm.MoveTo(x, y)
                dm.LeftClick()
                isFind = True
    for i in range(5):
        for j in range(6):
            PointX, PointY = 573 + 21 + 42 * i, 350 + 21 + 42 * j
            dm.MoveTo(PointX, PointY)
            s = items["未鉴定"]
            h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
            h, x, y = toInt(h, x, y)
            if x >= 0 and y >= 0:
                if j > 0:
                    unidentified_x, unidentified_y = 573 + 21 + 42 * i, 350 + 21 + 42 * (j - 1)
                else:
                    unidentified_x, unidentified_y = 573 + 21 + 42 * (i - 1), 350 + 22 + 42 * 5
                print("识别到：" + s[4] + ",坐标是:" + str(unidentified_x) + "," + str(unidentified_y))
                return unidentified_x, unidentified_y
            time.sleep(0.05)
    return unidentified_x, unidentified_y


def loginMenu():
    login = Tk()
    login.title('登录')
    login.geometry('210x150')
    Label(login, text='用户登录').grid(row=0, column=5, columnspan=2)
    Label(login, text='用户名：').grid(row=1, column=5)
    name = Entry(login)
    name.grid(row=1, column=6)
    Label(login, text='密码：').grid(row=2, column=5, sticky=E)
    passwd = Entry(login, show='*')
    passwd.grid(row=2, column=6)

    def make_password(password):
        # md5
        md5 = hashlib.md5()
        # 转码
        sign_utf8 = str(password).encode(encoding="utf-8")
        # 加密
        md5.update(sign_utf8)
        # 返回密文
        return md5.hexdigest()

    def center_window(root_info, width, height):
        screenwidth = root_info.winfo_screenwidth()  # 获取显示屏宽度
        screenheight = root_info.winfo_screenheight()  # 获取显示屏高度
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)  # 设置窗口居中参数
        root_info.geometry(size)  # 让窗口居中显示

    center_window(login, 210, 150)

    def successful():
        value = cf.get("account", name.get())
        print(value)
        if make_password(passwd.get()).__eq__(value):
            login.destroy()
            options_menu()
        else:
            messagebox.showerror(title='wrong', message='登录失败，用户名或密码错误')

    def options_menu():
        optionsMenu = Tk()
        optionsMenu.title('menu')
        optionsMenu.geometry('400x300')
        Label(optionsMenu, text='请选择你的操作：').grid(row=1, column=8, columnspan=2)
        Checkbutton(optionsMenu, text="刷图").grid(row=2, column=8, columnspan=2)
        # 单选框的返回值
        values = []
        menuNames = []
        menu_length = init_button(optionsMenu, values, menuNames)
        Button(optionsMenu, text='开始', command=lambda: startTask(values, menu_length, menuNames)).grid(
            row=len(values) + 2,
            column=8,
            columnspan=2)

        # 开始
        def startTask(valueList, menuLength, menuNameList):
            for i in range(menuLength):
                checkName = menuNameList[i]
                checkValue = valueList[i].get()
                if checkName.__eq__("鉴定背包"):
                    if checkValue == 1:
                        messagebox.showinfo("正在启动鉴定")
                        openQualification()
                if checkName.__eq__("日常副本"):
                    if checkValue == 1:
                        messagebox.showinfo("正在启动副本")
                        doTask()

        center_window(optionsMenu, 400, 300)
        optionsMenu.mainloop()

    # 动态加载按钮init.json的数据
    def init_button(optionMenu, values, menuNames):
        doTasks = root['menu']
        print(doTasks)
        i = 0
        for task in doTasks:
            values.append("val" + str(i))
            values[i] = IntVar()
            menuNames.append(task['text'])
            Checkbutton(optionMenu, text=task["text"], variable=values[i]).grid(row=i + 2, column=8,
                                                                                columnspan=2)
            i += 1
        return len(doTasks)

    Button(login, text='登录', command=successful).grid(row=3, column=6)

    def registrationMenu():
        registered = Tk()
        registered.title('registered')
        registered.geometry('230x185')
        Label(registered, text='用户注册').grid(row=0, column=0, columnspan=2)
        Label(registered, text='用户名：').grid(row=1, column=0, sticky=E)
        names = Entry(registered)
        names.grid(row=1, column=1)
        Label(registered, text='密码：').grid(row=2, column=0, sticky=E)
        passwords = Entry(registered, show='*')
        passwords.grid(row=2, column=1)
        Label(registered, text='确认密码：').grid(row=3, column=0)
        rePassword = Entry(registered, show='*')
        rePassword.grid(row=3, column=1)
        Label(registered, text='手机号：').grid(row=4, column=0, sticky=E)
        phoneNumber = Entry(registered)
        phoneNumber.grid(row=4, column=1)
        Label(registered, text='身份证号：').grid(row=5, column=0)
        man = Entry(registered)
        man.grid(row=5, column=1)
        center_window(registered, 230, 185)

        def registrationLogic():
            if len(passwords.get()) < 8:
                messagebox.showerror(title='wrong', message='注册失败，密码不应少于8位')
            elif passwords.get() != rePassword.get():
                messagebox.showerror(title='wrong', message='注册失败，两次密码不相同')
            else:
                cf.set("account", names.get(), make_password(passwords.get()))
                with open("./data.ini", 'w') as f:
                    cf.write(f)
                messagebox.showinfo(title='successful', message='注册成功！欢迎您。新会员')
                registered.destroy()

        Button(registered, text='注册', command=registrationLogic).grid(row=6, column=0, columnspan=2)

    Button(login, text='还没有账号？点我注册！', command=registrationMenu).grid(row=4, column=6, columnspan=2)
    login.mainloop()


def end():
    dm.UnBindWindow()


def 切换成比丘剑法():
    # 是不是比丘剑法
    pic = tpms["比丘剑法"]
    h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
    if x >= 0 and y >= 0:
        pass
    else:
        pic = tpms["剑普通攻击"]
        h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            dm.LeftClick()
            time.sleep(1)
            pic = tpms["比丘剑法1"]
            h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
            if x >= 0 and y >= 0:
                dm.MoveTo(x, y)
                dm.LeftClick()


def 进入草原():
    # 打开背包
    s = items["道具背包"]
    h, x, y = dm.FindStrFast(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    h, x, y = toInt(h, x, y)
    if x < 0 or y < 0:
        pic = tpms["状态栏下的背包按钮"]
        h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            dm.LeftClick()



if __name__ == '__main__':
    # loginMenu()
    # doTask()
    # openQualification()
    # checkStatus()
    进入草原()
    end()
