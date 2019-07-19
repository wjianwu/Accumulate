import time
import win32api

import win32con
from selenium import webdriver

from selenium_use import util, key_press


def open_chrome():
    # 加启动配置
    option = webdriver.ChromeOptions()
    option.add_argument("disable-infobars")
    option.add_argument("--start-maximized")
    # 打开浏览器
    create_driver = webdriver.Chrome(chrome_options=option)
    create_driver.get("https://uniportal.huawei.com")
    print("成功访问浏览器")
    time.sleep(3)
    return create_driver


def click_element(driver_arg, element, piv_x, piv_y):
    # 获取元素位置
    element_obj = driver_arg.find_element_by_xpath(element)
    element_position = element_obj.location_once_scrolled_into_view
    # 计算相对屏幕位置(浏览器窗口最大化)
    element_position["x"] = element_position["x"] + piv_x
    element_position["y"] = element_position["y"] + 70 + piv_y
    # 移动点击
    util.move_position((element_position["x"], element_position["y"]))
    util.left_click()
    time.sleep(3)


def get_verify_code(driver_arg):
    verify_code = driver_arg.find_element_by_xpath('//*[@id="verifycodeimage"]')
    # 保存验证码到本地
    time_str = str(int(time.time()))
    verify_code.screenshot("D:/verify_code/" + time_str + ".png")
    return "abcd"


def key_input(input_words=''):
    for word in input_words:
        win32api.keybd_event(key_press.VK_CODE[word], 0, 0, 0)
        win32api.keybd_event(key_press.VK_CODE[word], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.3)


def key_even(input_key):
    win32api.keybd_event(key_press.VK_CODE[input_key], 0, 0, 0)
    win32api.keybd_event(key_press.VK_CODE[input_key], 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)


if __name__ == '__main__':
    # 打开浏览器
    driver = open_chrome()
    # 点击注册
    click_element(driver, '//*[@id="button1"]', 60, 17)
    # 切换至手机注册
    click_element(driver, '//*[@id="tab_phone"]', 49, 20)
    # 点击手机号码框
    click_element(driver, '//*[@id="registerVO.officePhone"]', 115, 16)
    # 输入电话号码
    key_input("18279905201")
    time.sleep(0.5)
    # 输入密码
    key_even("tab")
    time.sleep(0.2)
    key_input("wjianwu666.")
    time.sleep(0.5)
    # 确认密码
    key_even("tab")
    time.sleep(0.2)
    key_input("wjianwu666.")
    time.sleep(0.2)
    # 准备输入验证码
    key_even("tab")
    time.sleep(5)
    key_input(get_verify_code(driver))
