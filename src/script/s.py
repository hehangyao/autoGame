from selenium import webdriver
import time
import datetime

browser = webdriver.Chrome()


# browser.maximize_window() 全屏浏览器
def login():
    browser.get("https://www.taobao.com")
    time.sleep(1.5)
    if browser.find_element_by_link_text("亲，请登录"):
        browser.find_element_by_link_text("亲，请登录").click()
        print(f"请尽快扫码登录")
        time.sleep(10) // 防查和不损被爬服务器

    # 跳转到购物车页面
    browser.get("https://cart.taobao.com/cart.htm")
    time.sleep(3)

    # 全选购物车
    while True:
        try:
            if browser.find_element_by_id("J_SelectAll1"):
                browser.find_element_by_id("J_SelectAll1").click()
                break
        except:
            print(f"没找到可以勾选商品")
    now = datetime.datetime.now()
    print('login successfully', now.strftime('%Y-%m-%d %H:%M:%S'))


def buy(buytime):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        if now > buytime:
            try:
                if browser.find_element_by_id("J_Go"):
                    browser.find_element_by_id("J_Go").click()
                browser.find_element_by_link_text("提交订单").click()
            except:
                time.sleep(0.1)
        print(now)
        time.sleep(0.1)


if __name__ == "__main__":
    login()
    buy("2021-5-6 15:00:00.000000")
