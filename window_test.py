import win32gui

# GetDesktopWindow 获得代表整个屏幕的一个窗口（桌面窗口）句柄
hd = win32gui.GetDesktopWindow()

# 获取所有子窗口
hwndChildList = []

win32gui.EnumChildWindows(hd, lambda hwnd, param: param.append(hwnd), hwndChildList)

for hwnd in hwndChildList:
    print("句柄：", hwnd, "标题：", win32gui.GetWindowText(hwnd))
    # f.write("句柄：" + str(hwnd) + " 标题：" + win32gui.GetWindowText(hwnd) + '\n')
