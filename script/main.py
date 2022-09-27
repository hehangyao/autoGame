# -*-coding:utf-8 -*-
import configparser
import random
import time
from tkinter import *
from tkinter import messagebox
import win32gui
from PyGameAutoFree import *
from init import *
from item import items
from script.enemys import enemyList
from tpms import tpms

tpms_new = toDict(tpms)
cf = configparser.ConfigParser()
cf.read("./data.ini")
param1 = cf.get("password", "param1")
param2 = cf.get("password", "param2")

# 框架初始化
dm = PyGameAuto.gl_init(param1, param2)
path = PyGameAuto.get_path(__file__)
需要捡的装备 = ["五色玉佩", "墨玉玉佩", "琥珀护身符", "红翡翠护身符", "蓝水晶戒指", "钻石戒指"]
# 句柄
hwnd = win32gui.FindWindow(None,
                           u"剑网贰单机版(交流QQ群:985964773)-此客户端与服务端免费分享 (公益怀旧群服专用客户端)")
# while hwnd <= 0:
#     print('未发现游戏窗口，请打开')
# hwnd = win32gui.FindWindow(None,
#                            u"剑网贰单机版(交流QQ群:985964773)-此客户端与服务端免费分享 (公益怀旧群服专用客户端)")
#     time.sleep(1)
ret = dm.BindWindow(hwnd, "dx", "dx", "dx", 1)
dm.SetDict(0, "new.txt")
status = ["初始化", "寻怪", "打怪", "捡装备"]
enemyNames = ["异族箭手", "异族武士", "精英异族箭手", "精英异族武士"]
enemyX, enemyY, enemyT = None, None, None
hero = {
    'x': 510,
    'y': 401
}


def 状态():
    dm.MoveTo(hero.get('x'), hero.get('y'))
    dm.LeftClick()
    加状态(65)  # a
    time.sleep(1)
    加状态(68)  # d
    time.sleep(1)
    加状态(81)  # q
    time.sleep(1)
    加状态(83)  # s
    time.sleep(1)
    加状态(87)  # w
    print("已加完状态")


def 加状态(key):
    dm.KeyPress(key)
    dm.MoveTo(hero.get('x'), hero.get('y'))
    dm.RightClick()
    time.sleep(1)
    print("加状态" + str(key))


def 找最近的怪():
    for i in enemyNames:
        s = enemyList[i]
        h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        if x >= 0 and y >= 0:
            return True, x, y, s[4]
    return False, -1, -1, None


def 找屏幕上的怪():
    for i in enemyNames:
        s = enemyList[i]
        h, x, y = dm.FindStr(0, 0, 1018, 670, s[4], s[5], s[6])
        if x >= 0 and y >= 0:
            return True, x, y, s[4]
    return False, -1, -1, None


def 找小地图近的怪():
    pic = tpms_new["怪小地图"]["怪小地图"]
    result = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
    h, x, y = result
    if x >= 0 and y >= 0:
        print("找到了：" + pic[4] + "地址：（" + str(x) + "," + str(y) + "）")
        return True, x, y, pic[4]
    else:
        return False, -1, -1, None


def 走路(di, step, t):
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


def 乱走():
    dis = ['L', 'R', 'U', 'D']
    # 随机一个方向和step
    dindex = random.randint(0, 3)
    print("dindex=" + str(dindex))
    step = random.randint(1, 3)
    times = random.randint(1, 8)
    走路(dis[dindex], step, times)
    time.sleep(2)


def 寻怪():
    isFind = False
    while not isFind:
        isFind, dx, dy, eType = 找最近的怪()
        if isFind:
            return dx, dy, eType
        else:
            isFind, dx, dy, eType = 找屏幕上的怪()
            if isFind:
                return dx, dy, eType
            else:
                isFind, dx, dy, eType = 找小地图近的怪()
                if isFind:
                    dm.MoveTo(dx + 1, dy + 1)
                    dm.LeftClick()
                    sleep(3)
                    isFind = False
                else:
                    乱走()
                    time.sleep(2)


点击怪次数 = {}


def 打怪(ex, ey):
    key = str(ex) + "," + str(ey)
    if key in 点击怪次数.keys():
        if 点击怪次数[key] > 3:
            return
        else:
            点击怪次数[key] += 1
    else:
        点击怪次数[key] = 1
    dm.MoveTo(ex + 50, ey + 70)
    dm.LeftClick()
    print("已点击%s,%s", str(ex + 50), str(ey + 70))


def 检查状态():
    pass


def doTask():
    time.sleep(2)
    print("辅助开始")
    stat = "初始化"
    x, y, etype = None, None, None
    while True:
        if stat.__eq__("初始化"):
            # 加状态
            状态()
            print("当前状态：" + stat)
            stat = "找怪"
        elif stat.__eq__("找怪"):
            # 找怪
            print("寻怪中。。。")
            x, y, etype = 寻怪()
            print("找到" + etype + ":(" + str(x) + "," + str(y) + ")")
            stat = "打怪"
        elif stat.__eq__("打怪"):
            # 打怪
            打怪(x, y)
            print("打怪中。。。：")
            stat = "捡装备"
        elif stat.__eq__("捡装备"):
            # 捡装备
            捡装备()
            print("当前状态：" + stat)
            stat = "检查状态"
        elif stat.__eq__("检查状态"):
            # 检查状态
            检查状态()
            print("当前状态：" + stat)
            stat = "找怪"


def 捡装备():
    for i in 需要捡的装备:
        s = items[i]
        h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        if x >= 0 and y >= 0:
            dm.MoveTo(x, y)
            print("识别到：" + s[4] + ",坐标是:" + str(x) + "," + str(y))
            dm.LeftClick()
            sleep(2)
            打开鉴定()


def 打开鉴定():
    未鉴定x, 未鉴定y = 查找未鉴定装备()
    if 未鉴定x >= 0 and 未鉴定y >= 0:
        s = items["道具背包"]
        h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        if x < 0 or y < 0:
            dm.MoveTo(hero.get('x'), hero.get('y'))
            dm.LeftClick()
            dm.KeyPress(115)  # F4
            time.sleep(0.5)
        s = items["扩展背包"]
        h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        if x < 0 or y < 0:
            pic = tpms_new["扩展背包按钮"]["扩展背包按钮"]
            isFind = False
            while not isFind:
                h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
                if x >= 0 and y >= 0:
                    dm.MoveTo(x, y)
                    dm.LeftClick()
                    isFind = True
        pic = tpms_new["七级鉴定符"]["七级鉴定符"]
        isFind = False
        while not isFind:
            h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
            if x >= 0 and y >= 0:
                dm.MoveTo(x + 22, y + 22)
                time.sleep(0.5)
                dm.RightClick()
                time.sleep(0.5)
                dm.MoveTo(304, 230)
                dm.MoveTo(未鉴定x, 未鉴定y)
                dm.LeftClick()
                isFind = True


def 查找未鉴定装备():
    未鉴定X, 未鉴定Y = -1, -1
    # 815,367,1017,613,宽高(202,246)
    s = items["道具背包"]
    h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    if x < 0 or y < 0:
        dm.KeyPress(115)  # F4
        time.sleep(0.5)
    for i in range(5):
        for j in range(6):
            PointX, PointY = 815 + 22 + 40 * i, 367 + 22 + 40 * j
            dm.MoveTo(PointX, PointY)
            s = items["未鉴定"]
            h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
            if x >= 0 and y >= 0:
                if j > 0:
                    未鉴定X, 未鉴定Y = 815 + 22 + 40 * i, 367 + 22 + 40 * (j - 1)
                else:
                    未鉴定X, 未鉴定Y = 815 + 22 + 40 * (i - 1), 367 + 22 + 40 * 5
                print("识别到：" + s[4] + ",坐标是:" + str(未鉴定X) + "," + str(未鉴定Y))
                return 未鉴定X, 未鉴定Y
            time.sleep(0.3)
    s = items["扩展背包"]
    h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
    if x < 0 or y < 0:
        pic = tpms_new["扩展背包按钮"]["扩展背包按钮"]
        isFind = False
        while not isFind:
            h, x, y = dm.FindPic(pic[0], pic[1], pic[2], pic[3], pic[4], pic[5], pic[6])
            if x >= 0 and y >= 0:
                dm.MoveTo(x, y)
                dm.LeftClick()
                isFind = True
    time.sleep(1)
    for i in range(5):
        for j in range(6):
            PointX, PointY = 598 + 22 + 40 * i, 367 + 22 + 40 * j
            dm.MoveTo(PointX, PointY)
            s = items["未鉴定"]
            h, x, y = dm.FindStr(s[0], s[1], s[2], s[3], s[4], s[5], s[6])
            if x >= 0 and y >= 0:
                if j > 0:
                    未鉴定X, 未鉴定Y = 598 + 22 + 40 * i, 367 + 22 + 40 * (j - 1)
                else:
                    未鉴定X, 未鉴定Y = 598 + 22 + 40 * (i - 1), 367 + 22 + 40 * 5
                print("识别到：" + s[4] + ",坐标是:" + str(未鉴定X) + "," + str(未鉴定Y))
                return 未鉴定X, 未鉴定Y
            time.sleep(0.3)
    return 未鉴定X, 未鉴定Y


def memus():
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

    def center_window(root, width, height):
        screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
        screenheight = root.winfo_screenheight()  # 获取显示屏高度
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)  # 设置窗口居中参数
        root.geometry(size)  # 让窗口居中显示

    center_window(login, 210, 150)

    def successful():
        if name.get() == 'admin' and passwd.get() == 'admin':
            login.destroy()
            menu()
        else:
            messagebox.showerror(title='wrong', message='登录失败，用户名或密码错误')

    def menu():
        menu = Tk()
        menu.title('menu')
        menu.geometry('400x300')
        Label(menu, text='请选择你的操作：').grid(row=1, column=8, columnspan=2)
        Checkbutton(menu, text="刷图").grid(row=2, column=8, columnspan=2)
        # 单选框的返回值
        values = []
        menuNames = []
        menulenth = init_button(menu, values, menuNames)
        Button(menu, text='开始', command=lambda: startTask(values, menulenth, menuNames)).grid(row=len(values) + 2,
                                                                                                column=8,
                                                                                                columnspan=2)

        # 开始
        def startTask(values, menulenth, menuNames):
            for i in range(menulenth):
                checkName = menuNames[i]
                checkValue = values[i].get()
                if checkName.__eq__("鉴定背包"):
                    if checkValue == 1:
                        messagebox.showinfo("正在启动鉴定")
                        打开鉴定()
                if checkName.__eq__("日常副本"):
                    if checkValue == 1:
                        messagebox.showinfo("正在启动副本")
                        doTask()

        center_window(menu, 400, 300)
        menu.mainloop()

    # 动态加载按钮init.json的数据
    def init_button(menu, values, menuNames):
        roots = toDict(root)
        print(roots)
        doTasks = roots['menu']['menu']
        print(doTasks)
        i = 0
        for doTask in doTasks:
            values.append("val" + str(i))
            values[i] = IntVar()
            menuNames.append(doTask['text'])
            Checkbutton(menu, text=doTask["text"], variable=values[i]).grid(row=i + 2, column=8,
                                                                            columnspan=2)
            i += 1
        return len(doTasks)

    Button(login, text='登录', command=successful).grid(row=3, column=6)

    def registereds():
        registered = Tk()
        registered.title('registered')
        registered.geometry('230x185')
        Label(registered, text='用户注册').grid(row=0, column=0, columnspan=2)
        Label(registered, text='用户名：').grid(row=1, column=0, sticky=E)
        names = Entry(registered)
        names.grid(row=1, column=1)
        Label(registered, text='密码：').grid(row=2, column=0, sticky=E)
        passwds = Entry(registered, show='*')
        passwds.grid(row=2, column=1)
        Label(registered, text='确认密码：').grid(row=3, column=0)
        repasswd = Entry(registered, show='*')
        repasswd.grid(row=3, column=1)
        Label(registered, text='手机号：').grid(row=4, column=0, sticky=E)
        phonenum = Entry(registered)
        phonenum.grid(row=4, column=1)
        Label(registered, text='身份证号：').grid(row=5, column=0)
        man = Entry(registered)
        man.grid(row=5, column=1)
        center_window(registered, 230, 185)

        def teshufuhao(input_psd):
            string = "~!@#$%^&*()_+-*/<>,.[]\/"
            for i in string:
                if i in input_psd:
                    return True
            return False

        def registeredes():
            if not (any([x.isdigit() for x in names.get()]) and any([x.isalpha() for x in names.get()]) and teshufuhao(
                    names.get())):
                messagebox.showerror(title='wrong', message='注册失败，用户名格式错误，必须包括字母和数字以及特殊符号')
            elif len(passwds.get()) < 8:
                messagebox.showerror(title='wrong', message='注册失败，密码不应少于8位')
            elif passwds.get() != repasswd.get():
                messagebox.showerror(title='wrong', message='注册失败，两次密码不相同')
            elif not (phonenum.get().isdigit() and len(phonenum.get()) == 11):
                messagebox.showerror(title='wrong', message='注册失败，请输入正确的11位手机号')
            elif len(man.get()) != 18:
                messagebox.showerror(title='wrong', message='注册失败，请输入正确的18位身份证号')
            else:
                messagebox.showinfo(title='successful', message='注册成功！欢迎您。新会员')

        Button(registered, text='注册', command=registeredes).grid(row=6, column=0, columnspan=2)

    Button(login, text='还没有账号？点我注册！', command=registereds).grid(row=4, column=6, columnspan=2)
    login.mainloop()


if __name__ == '__main__':
    print("11111")
