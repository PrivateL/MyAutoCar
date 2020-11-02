import pyautogui as pg
import win32gui, win32api, win32con
import time
import random


# windows api的截图功能


# # pyautogui的截图功能(初次18.32s/100张，之后12s-15s)
# for i in range(100):
#     pg.screenshot('../screenshot/img_%s.png'%str(i))

# # 切屏到游戏界面
# win32api.keybd_event(18, 0, 0, 0)
# win32api.keybd_event(9, 0, 0, 0)
# win32api.keybd_event(9, 0, win32con.KEYEVENTF_KEYUP, 0)
# win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
# time.sleep(0.1)
# # 按回车开始游戏
# win32api.keybd_event(13, 0, 0, 0)
# win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)


def move(direct: str, speed: int):
    code = 37
    if direct == 'left':
        code = 37
    elif direct == 'up':
        code = 38
    elif direct == 'right':
        code = 39
    elif direct == 'down':
        code = 40
    win32api.keybd_event(code, 0, 0, 0)
    time.sleep(0.06 + 0.02 * speed)  # speed=0时，左右(上下)移动20(12)单位，speed每加一，约多移动5(3)单位
    win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)


'''
time.sleep(1)
yellow_car = '../other/yellow_car.png'
blue_car = '../other/blue_car.png'
for sp in range(5):
    start = time.time()
    res = []
    for i in range(6):
        if i < 3:
            move('left', sp)
        else:
            move('right', sp)
        pos = pg.locateOnScreen(yellow_car)
        res.append(pos.left)
        time.sleep(1)
    print("speed:", sp, res)
    print(time.time() - start)
'''
# pg.hotkey('alt', 'tab')

#
# pg.press('up')
# pg.press('down')
# pg.press('enter')
# pg.press('left')
# pg.press('right')
# pg.hotkey('ctrl', 'v')
