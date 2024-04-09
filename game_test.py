import math
import time

import pyautogui
import pydirectinput as direct
import win32gui
from ultralytics import YOLO

from util import get_window_location_info, get_window_screen_shot, draw_frame_and_save

'''
注意：需要使用【管理员】权限运行时，pydirectinput 模块才会生效
'''

direct.PAUSE = False
model = YOLO('../best.pt')

width, height = pyautogui.size()
hwnd = win32gui.FindWindow(0, win32gui.GetWindowText(526408))
print(hwnd)
x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
w = x2 - x1
h = y2 - y1
# 获取窗口中心点坐标 (mp[0], mp[1])
mp = (width / 2, height / 2)
print('start....')
while True:
    image = get_window_screen_shot(526408)
    print("拍摄了图片...")
    result = model(source=image, device=0, classes=0)
    boxes = result[0].boxes
    point = None
    rect_info_list = []
    distance = 999999
    for box in boxes:
        cls = box.cls.cpu().numpy().tolist()[0]
        conf = boxes.conf.cpu().numpy().tolist()[0]
        if int(cls) == 0 and conf >= 0.6:
            points = box.xyxy.cpu().numpy().tolist()[0]
            x1, y1, x2, y2 = points
            # temp_point 表示识别出来的矩形框中点的相对坐标
            temp_point = (x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 4)
            # 距离准心的距离
            temp_distance = math.sqrt(math.pow((temp_point[0] - mp[0]), 2) + math.pow(temp_point[1] - mp[1], 2))
            rect_info_list.append(points)
            if temp_distance < distance:
                point = temp_point
                distance = temp_distance
                print("更新坐标：{:>5},{:>5}，距离：{}".format(point[0], point[1], distance))
    if point and distance <= 200:
        print("射击...")
        xOffset = int(point[0] - mp[0])
        yOffset = int(point[1] - mp[1])
        # 移动准心
        direct.moveRel(xOffset=xOffset, yOffset=yOffset, relative=True)
        direct.mouseDown()
        time.sleep(0.3)
        direct.mouseUp()
        # 绘制
        # draw_frame_and_save(rect_info_list, image, point)
    else:
        print("未识别到结果...")
