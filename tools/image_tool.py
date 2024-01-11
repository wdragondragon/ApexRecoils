from PIL import ImageGrab
import configparser
from pynput.keyboard import Controller, Listener

config = configparser.ConfigParser()  # 创建对象
config.read("image_tool.conf", encoding="utf-8")

# screen = tkinter.Tk()  # 这里首先利用tk视图ui框架获取分辨率
# xw = screen.winfo_screenwidth()
# 获取当前屏幕的宽
# yh = screen.winfo_screenheight()
# 获取当前屏幕的高

# 睡眠1秒 给自己留时间打开需要打开的页面
# time.sleep(1)
# print('获取当前屏幕', xw, yh)

path = config.get("conf", "path")  # 需要保存到E盘的目录文件名
bbox = tuple(int(x) for x in config.get("conf", "bbox").split(","))
print_screen_key = config.get("conf", "print_screen_key")
# 整个屏幕截图，也可以指定x、y坐标进行截图
# img = ImageGrab.grab(bbox=(100, 500, xw, yh)) 表示从x轴坐标100开始，y轴500开始

keyboard = Controller()


def on_press(key):
    # print('{0} 被按下'.format(key))
    pass


# 释放按钮，按esc按键会退出监听
def on_release(key):
    # print('{0} 被释放'.format(key))
    if not hasattr(key, 'name') and (key.char == print_screen_key):
        img = ImageGrab.grab(bbox=bbox)  # 也可以不传参数，默认截取整个屏幕
        img.save(path)  # 保存到E盘目录
        print('截图保存成功')


# 创建监听
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# imsrc = ac.imread(path)  # 需要用aircv转换，方便cv2.imshow函数打开
# cv2.imshow('python屏幕截图后自动打开该图片', imsrc)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
