import cv2

from core.screentaker.ScreenTaker import ScreenTaker
from log import LogFactory


class CapScreenTaker(ScreenTaker):
    """
        本地截图
    """

    def __init__(self, cap_param):
        self.logger = LogFactory.getLogger(self.__class__)
        self.width = cap_param["width"]
        self.height = cap_param["height"]
        self.frame_rate = cap_param["frame_rate"]
        self.format = cap_param["format"]
        self.cap = cv2.VideoCapture(0)  # 视频流
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.frame_rate)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*self.format))
        self.logger.print_log(f"使用视频采集卡：{cap_param}")

    def get_images_from_bbox(self, bbox_list):
        frames = []
        ret, frame = self.cap.read()
        for monitor in bbox_list:
            frames.append(frame[monitor[1]: monitor[3], monitor[0]: monitor[2]])
        return list(frames)
