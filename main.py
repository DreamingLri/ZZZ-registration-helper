import cv2
import numpy as np
import pyautogui as pag
import time
from datetime import datetime

login = cv2.imread('image/image-1.png', cv2.IMREAD_GRAYSCALE)
go_back = cv2.imread('image/image-2.png', cv2.IMREAD_GRAYSCALE)
sleep = cv2.imread('image/image-3.png', cv2.IMREAD_GRAYSCALE)

w1, h1 = login.shape[::-1]
w2, h2 = go_back.shape[::-1]
w3, h3 = sleep.shape[::-1]

coordinates = {
    'login': (960, 586),
    'go_back': (700, 676),
    'sleep': (960, 676)
}

thresholds = {
    'login': 0.5,
    'go_back': 0.8,
    'sleep': 0.9
}

def counter(seconds):
    for i in range(seconds, 0, -1):
        print(f" {i} 秒后开始识别...")
        time.sleep(1)

def start():
    print("欢迎使用绝区零自动注册器!")
    # print("请选择您的屏幕大小: 1. 1920x1080 2. 1920x1080以上")
    # choice = input("请输入您的选择: ")
    # global screenshot_region
    # if(choice == "1"):
    #     screenshot_region = (0, 0, 1278, 759)
    # else:
    #     screenshot_region = (0, 0, 1920, 1127)

    print("请确保您已经打开了绝区零，并且在登录界面")
    print("请将您的绝区零设置为1920x1080窗口模式，并拖到屏幕左上角，且前方无遮挡")
    print("现在进行按钮注册")

    print("--------------------------------------")
    print("请将鼠标移动到--点击进入游戏--")
    print("按Enter开始识别")
    input()

    counter(3)
    x, y = pag.position()
    print(f"坐标为: ({x}, {y})")
    coordinates['login'] = (x, y)
    pag.click()

    print("--------------------------------------")
    print("请将鼠标移动到--取消--")
    print("按Enter开始识别")
    input()

    counter(3)
    x, y = pag.position()
    print(f"坐标为: ({x}, {y})")
    coordinates['go_back'] = (x, y)
    pag.click()

    print("按Enter继续")
    input()

    print("请连续登录，触发风控，显示--您的操作过于频繁，请稍后再试--")

    print("--------------------------------------")
    print("按Enter继续")
    input()

    print("--------------------------------------")
    print("请将鼠标移动到--确认--")
    print("按Enter开始识别")
    input()
    counter(3)
    x, y = pag.position()
    print(f"坐标为: ({x}, {y})")
    coordinates['sleep'] = (x, y)

    print("请回到开始界面，按Enter开始自动挂机")
    input()

def match_and_click(template, coord, template_name, threshold):
    screenshot = pag.screenshot(region=(0, 46, 1920, 1080))
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
    
start()
while True:
    if match_and_click(sleep, coordinates['sleep'], '风控页面', thresholds['sleep']):
        current_time = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        print(f"{current_time} 检测到被风控！休眠15秒")
        time.sleep(15)
    
    match_and_click(login, coordinates['login'], '登录主页面', thresholds['login'])
    time.sleep(1)
    match_and_click(go_back, coordinates['go_back'], '取消', thresholds['go_back'])
    time.sleep(6.6)
