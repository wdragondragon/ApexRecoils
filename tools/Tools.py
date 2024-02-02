import ctypes
import os
import queue
import threading
import time
from io import BytesIO
from shutil import copyfile

import cv2
import numpy as np
import win32gui
from skimage.metrics import structural_similarity
from collections import deque


class Tools:
    """
        工具类
    """

    @staticmethod
    def get_resolution():
        """
            获取当前屏幕分辨率
        :return:
        """
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware(2)
        [xw, yh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        return xw, yh

    @staticmethod
    def compare_image(img, path_image):
        """
            图片对比
        :param img:
        :param path_image:
        :return:
        """
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        image_a = cv2.imdecode(np.frombuffer(buffer.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
        buffer.close()
        image_b = cv2.imdecode(np.fromfile(path_image, dtype=np.uint8), cv2.IMREAD_COLOR)
        gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        (score, diff) = structural_similarity(gray_a, gray_b, full=True)
        return score

    @staticmethod
    def current_milli_time():
        """
            获取当前时间戳13位
        :return:
        """
        return int(round(time.time() * 1000))

    @staticmethod
    def copy_file(source_path, target_path):
        """
            复制文件
        :param source_path:
        :param target_path:
        """
        op = os.path
        if isinstance(source_path, str):
            if op.exists(source_path):
                copyfile(source_path, target_path)
            else:
                print("源文件不存在")

    @staticmethod
    def convert_to_decimal(input_str):
        try:
            # 尝试将输入字符串解析为16进制数字
            decimal_value = int(input_str, 16)
        except ValueError:
            try:
                # 如果解析失败，则尝试将输入字符串解析为10进制数字
                decimal_value = int(input_str, 10)
            except ValueError:
                # 如果两者都失败，返回一个适当的错误或默认值
                # print("无法解析输入字符串为数字")
                return None

        return decimal_value

    @staticmethod
    def is_apex_windows():
        """
            是否处于apex窗口中
        :return:
        """
        window_handle = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(window_handle)
        return window_title == 'Apex Legends'

    class FixedSizeQueue:
        """
            固定长度队列
        """

        def __init__(self, max_size):
            self.queue = deque(maxlen=max_size)

        def push(self, item):
            """
                将数据入队
            :param item:
            """
            self.queue.append(item)

        def pop(self):
            """
                出队最先入队的数据
            :return:
            """
            return self.queue.popleft()

        def size(self):
            """
                获取队列当前数据量
            :return:
            """
            return len(self.queue)

        def get_last(self):
            """
                获取最后入队的数据，不出队
            :return:
            """
            # 获取最后一次进队的元素但不出队
            return self.queue[-1] if self.queue else None

    class GetBlockQueue:
        """
            阻塞队列
        """

        def __init__(self, name, maxsize=1):
            self.name = name
            self.lock = threading.Lock()
            self.queue = queue.Queue(maxsize=maxsize)

        def get(self):
            o = self.queue.get()
            return o

        def put(self, data):
            with self.lock:
                while True:
                    try:
                        self.queue.put(data, block=False)
                        break
                    except queue.Full:
                        try:
                            self.queue.get_nowait()
                        except queue.Empty:
                            pass

        def clear(self):
            with self.lock:
                while not self.queue.empty():
                    self.queue.get()
