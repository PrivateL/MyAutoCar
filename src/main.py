import pyautogui as pg
from collections import namedtuple
import time

from tool.control_keyboard import move


class Window:
    def __init__(self):
        # 切屏到游戏界面
        pg.hotkey('alt', 'tab')
        # 定位游戏区域
        self.__game_region = self.__get_game_region()
        # 按回车开始游戏
        pg.press('enter')

    # 定位游戏区域
    def __get_game_region(self):
        timeout = 10
        left_top = right_btn = None
        while left_top is None or right_btn is None:
            left_top = pg.locateCenterOnScreen('../other/window_left_top.png')  # 左上角
            right_btn = pg.locateCenterOnScreen('../other/window_right_button.png')  # 右下角
            timeout -= 1
            if timeout == 0:  # 超时未找到游戏区域
                print("class Window: 获取游戏区域超时!!!")
                Location = namedtuple('Location', ['x', 'y'])
                left_top = Location(478, 91)  # 默认为浏览器全屏运行在本人笔记本上时的坐标
                right_btn = Location(820, 716)
                break
        self.width = right_btn.x - left_top.x
        self.height = right_btn.y - left_top.y
        region = (left_top.x, left_top.y, self.width, self.height)
        wd = pg.screenshot(region=region)
        wd.save('../screenshot/window.png')
        return region

    def get_game_region(self):
        return self.__game_region


class YellowCar:
    def __init__(self, game_region):
        self.game_region = game_region
        self.yellow_car_png = '../other/yellow_car.png'  # 30*50px(四周各少5px)
        self.top = self.game_region[1] + 5  # 设置默认值
        self.width = 40
        self.height = 60
        self.move_region = self.__get_car_move_region()

    # 定位黄色小车的移动区域（当前版本仅左右平移）
    def __get_car_move_region(self):
        timeout = 10
        rg_h = self.height
        while self.top == self.game_region[1] + 5:
            yellow_car = pg.locateOnScreen(self.yellow_car_png, region=self.game_region)
            if yellow_car is not None:
                self.top = yellow_car.top
            timeout -= 1
            if timeout == 0:
                print("class YellowCar: 获取黄色小车的区域超时!!!")
                rg_h = self.game_region[3]
                break
        region = (self.game_region[0], self.top - 5, self.game_region[2], rg_h)
        return region

    # 黄色小车的坐标
    def get_location(self):
        pos = pg.locateOnScreen(self.yellow_car_png, region=self.move_region)
        if pos is None:
            return None
        Location = namedtuple('Location', ['x', 'y'])
        return Location(pos.left - 5, pos.top - 5)


class BlueCar:
    def __init__(self, game_region):  # 游戏区域和黄色小车的平移区域
        self.game_region = game_region
        self.blue_car_png = '../other/blue_car.png'  # 30*50px(四周各少5px)
        self.width = 40
        self.height = 60

    # 蓝色小车的坐标
    def get_all_location(self):
        Location = namedtuple('Location', ['x', 'y'])
        while True:
            all_pos = pg.locateAllOnScreen(self.blue_car_png, region=self.game_region)
            res = []
            for pos in all_pos:
                res.append(Location(pos.left - 5, pos.top - 5))
            if len(res) > 0:
                return res


def get_aim(arr: list, width, yellow_x):
    arr.sort()
    size = len(arr)
    res = 10000
    for i in range(size - 1):
        if arr[i + 1] - arr[i] - 2 * width > 15:
            a = (arr[i + 1] + width + arr[i]) // 2
            if abs(yellow_x - a) < abs(yellow_x - res):
                res = a
    if res == 10000:
        return yellow_x
    else:
        return res - width//2


if __name__ == "__main__":
    win_region = Window().get_game_region()
    print("游戏窗口：", win_region)
    move('up', 3)  # 上移一点点，腾出空间，避免与小车尾部相撞

    start = time.time()
    yellow_car = YellowCar(win_region)
    print("获取黄色小车平移区域：", yellow_car.move_region, "耗时：", time.time() - start)
    blue_car = BlueCar(win_region)

    while True:
        start = time.time()
        y_loc = yellow_car.get_location()
        if not y_loc:
            break
        print("获取黄色小车坐标", y_loc, "耗时：", time.time() - start)

        start = time.time()
        b_loc = blue_car.get_all_location()
        print("获取所有蓝色小车坐标", b_loc, "耗时：", time.time() - start)

        b_loc_x = [i.x for i in b_loc]
        loc_x = [win_region[0] - blue_car.width] + b_loc_x + [win_region[0] + win_region[2]]

        # aim = y_loc.x
        # if b_loc[0].y + blue_car.height < y_loc.y:
        #     aim = (b_loc_x[0]+win_region[0])//2 if b_loc[0].x > win_region[0]+win_region[2]//2 else (b_loc[0].x+loc_x[-1])//2
        # if len(b_loc_x) > 1:
        #     aim = get_aim(loc_x, blue_car.width, y_loc.x)
        aim = get_aim(loc_x, blue_car.width, y_loc.x)
        bias = 8  # 与目标位置的误差在8以内可以不移动
        times = (abs(aim-y_loc.x) + 20-bias) // 20
        for i in range(times):
            if aim < y_loc.x:
                move('left', 0)
            elif aim > y_loc.x:
                move('right', 0)

    pg.hotkey('alt', 'tab')
