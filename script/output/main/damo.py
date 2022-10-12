import time

import win32gui
from PyGameAutoFree import PyGameAuto

# 1．注册
dm = PyGameAuto.gl_init("xf30557fc317f617eead33dfc8de3bdd4ab9043", "xfqphyzoxouw700")
path = PyGameAuto.get_path(__file__)
print(path)
# 句柄
hwnd = win32gui.FindWindow(None,
                           u"126网易免费邮-你的专业电子邮局 - Google Chrome")
print(hwnd)
hwnd = int(hwnd)
path = PyGameAuto.get_path(__file__)
dm.SetPath(path)
# 3．激活并绑定窗口
dm_ret = dm.BindWindow(hwnd, "dx", "windows3", "windows", 101)
ret = dm.SetWindowState(hwnd, 1)
dm.SetWindowSize(int(hwnd), 800, 600)
dm.MoveWindow(hwnd, 0, 0)
time.sleep(1)

# 4．执行动作
ret = dm.FindPic(0, 0, 2000, 2000, u"./登录.bmp", "010101", 0.9, 1)
t, x, y = ret
print(ret)
ret = dm.MoveTo(x, y)
print(x, y)
dm.LeftClick()
# 5．解绑
dm.UnBindWindow()
