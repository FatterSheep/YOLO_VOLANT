import tempfile
import time

import win32con
import win32gui
import pyautogui

import detect

width, height = pyautogui.size()
hwnd = win32gui.FindWindow(0, win32gui.GetWindowText(1705844))
print(hwnd)

# if win32gui.IsWindow(hwnd):
#     # 设置窗口为可见状态
#     win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
#     # 将窗口置于前台
#     win32gui.SetForegroundWindow(hwnd)
#
#     # win32gui.GetWindowRect(hwnd)
# else:
#     print('窗口无效')

x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
w = x2 - x1
h = y2 - y1

while True:
    if w > 0 and h > 0:
        time.sleep(1)
        region = (x1, y1 + 30, int(w), int(h))
        print(region)
        im = pyautogui.screenshot(region=region)
        print(im)
        # im.show()

        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        # 将Image对象保存到临时文件
        im.save(temp_file.name)
        # 将临时文件的路径传递给需要文件路径的函数
        file_path = temp_file.name
        # your_function(file_path)
        img = detect.parse_opt(file_path)
        i = detect.main(img)
        # 关闭临时文件
        temp_file.close()

    else:
        print('invalid rect info')



