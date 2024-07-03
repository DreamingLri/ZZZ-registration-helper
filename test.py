import win32gui as win
import time
import pyautogui as pag

time.sleep(3)
window = win.FindWindow(None, "绝区零")
x_1, y_1, x_2, y_2 = win.GetWindowRect(window)
screenshot = pag.screenshot(region=(x_1, y_1, x_2 - x_1, y_2 - y_1))
screenshot.save("image.png")
print(x_2, x_1, y_2, y_1)