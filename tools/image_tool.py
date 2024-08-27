import cv2
import numpy as np
from PIL import ImageGrab
import configparser
from pynput.keyboard import Controller, Listener

from core.screentaker.CapScreenTaker import CapScreenTaker
from log import LogFactory

config = configparser.ConfigParser()  # 创建对象
config.read("image_tool.conf", encoding="utf-8")
path = config.get("conf", "path")  # 需要保存到E盘的目录文件名
bbox = tuple(int(x) for x in config.get("conf", "bbox").split(","))
print_screen_key = config.get("conf", "print_screen_key")
keyboard = Controller()
i = 1

LogFactory.init_logger()

screen_taker = CapScreenTaker({
    "width": 2560,
    "height": 1440,
    "frame_rate": 144,
    "format": "MJPG"
})


def on_press(key):
    # print('{0} 被按下'.format(key))
    pass


# 释放按钮，按esc按键会退出监听
def on_release(key):
    # print('{0} 被释放'.format(key))
    global i

    if not hasattr(key, 'name') and (key.char == print_screen_key):
        # img = ImageGrab.grab(bbox=bbox)  # 也可以不传参数，默认截取整个屏幕
        # img.save(path + str(i) + ".png")  # 保存到E盘目录

        img = screen_taker.get_images_from_bbox([bbox])[0]
        img = np.array(img)
        cv2.imwrite(path + str(i) + ".png", img)

        print('截图保存成功')
        i += 1


# 创建监听
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# imsrc = ac.imread(path)  # 需要用aircv转换，方便cv2.imshow函数打开
# cv2.imshow('python屏幕截图后自动打开该图片', imsrc)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
