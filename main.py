import cv2
import win32gui as win
import numpy as np
import pyautogui as pag
from datetime import datetime
import time


def get_current_window():

    window = win.FindWindow(None, "绝区零")
    x_1, y_1, x_2, y_2 = win.GetWindowRect(window)

    s_1 = (y_2 - y_1) / 2.29 + y_1
    s_2 = (y_2 - y_1) / 1.45 + y_1

    global screenshot_position
    screenshot_position = (int(x_1), int(s_1), int(x_2 - x_1), int(s_2 - s_1))

    print(x_2 - x_1, y_2 - y_1)

    s4 = (y_2 - y_1) / 1.65 + y_1
    s3 = (x_2 - x_1) / 2 + x_1
    global coordinates
    coordinates = {
        'login': (s3, s4),
        'go_back': (s3 - 145, s4),
        'sleep': (s3, s4)
    }


coordinates = {
    'login': (960, 586),
    'go_back': (700, 676),
    'sleep': (960, 676)
}

screenshot_position = (0, 0, 1920, 1080)

thresholds = {
    'login': 0.3,
    'go_back': 0.4,
    'sleep': 0.4
}

login = cv2.imread('image/image1.png', cv2.IMREAD_GRAYSCALE)
go_back = cv2.imread('image/image2.png', cv2.IMREAD_GRAYSCALE)
sleep = cv2.imread('image/image3.png', cv2.IMREAD_GRAYSCALE)

# pag.click(s3, s4)
# screenshot.save("image3.png")

def match_and_click(template, coord, template_name, threshold):
    screenshot = pag.screenshot(region=screenshot_position)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{current_time} 正在尝试匹配 {template_name}，最大匹配相似度 = {max_val}")

    if max_val >= threshold:
        print(f"{current_time} 当前页面成功以最大匹配相似度 {max_val} 匹配上了 {template_name}，正在点击位置 {coord}")
        pag.moveTo(coord[0], coord[1])
        pag.click()
        return True
    else:
        print(f"{current_time} 当前页面看起来不像 {template_name}，最大匹配相似度为 {max_val}")
        return False

while True:
    get_current_window()
    if match_and_click(sleep, coordinates['sleep'], '风控页面', thresholds['sleep']):
        current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        print(f"{current_time} 检测到被风控！休眠15秒")
        time.sleep(15)
    
    match_and_click(login, coordinates['login'], '登录主页面', thresholds['login'])
    time.sleep(1)
    match_and_click(go_back, coordinates['go_back'], '取消', thresholds['go_back'])
    time.sleep(6.6)

    