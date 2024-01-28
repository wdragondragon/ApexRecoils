import os
import threading
import time
import traceback

from PIL import ImageGrab

from core.KeyAndMouseListener import KMCallBack
from core.ImageComparator import ImageComparator
from net.socket.NetImageComparator import NetImageComparator
from tools.Tools import Tools
from log.Logger import Logger
from io import BytesIO

import cv2
import numpy as np
from skimage.metrics import structural_similarity


class SelectGun:
    """
        枪械识别
    """

    def __init__(self, logger: Logger, bbox, image_path, scope_bbox, scope_path, hop_up_bbox, hop_up_path,
                 refresh_buttons, has_turbocharger, net_comparator):
        super().__init__()
        self.logger = logger
        self.on_key_map = dict()
        self.bbox = bbox
        self.image_path = image_path
        self.scope_bbox = scope_bbox
        self.scope_path = scope_path
        self.select_gun_sign = False
        self.current_gun = None
        self.current_scope = None
        self.current_hot_pop = None
        self.refresh_buttons = refresh_buttons
        self.has_turbocharger = has_turbocharger
        self.hop_up_bbox = hop_up_bbox
        self.hop_up_path = hop_up_path
        self.call_back = []
        self.fail_time = 0

        self.net_comparator = net_comparator
        if net_comparator:
            self.image_comparator = NetImageComparator(logger)
        else:
            self.image_comparator = LocalImageComparator(logger)
        for refresh_button in self.refresh_buttons:
            KMCallBack.connect(KMCallBack("k", refresh_button, self.select_gun_threading, False))

        threading.Thread(target=self.timing_execution).start()

    def timing_execution(self):
        while True:
            try:
                if self.select_gun_with_sign(auto=True):
                    self.fail_time = 0
                else:
                    self.fail_time += 1
            except Exception as e:
                traceback.print_exc()
                pass
            time.sleep(1 + self.fail_time / 5)

    def select_gun_threading(self, pressed=False, toggle=False):
        if self.select_gun_sign:
            return
        threading.Thread(target=self.select_gun_with_sign, args=(pressed, toggle, False)).start()

    def select_gun_with_sign(self, pressed=False, toggle=False, auto=False):
        if self.select_gun_sign:
            return
        self.select_gun_sign = True
        start = time.time()
        result = self.select_gun(pressed, toggle, auto)
        self.logger.print_log(f"该次识别耗时：{int((time.time() - start) * 1000)}ms")
        self.select_gun_sign = False
        return result

    def select_gun(self, pressed=False, toggle=False, auto=False):
        """
            使用图片对比，逐一识别枪械，相似度最高设置为current_gun
        :return:
        """
        gun_temp, score_temp = self.image_comparator.compare_with_path(self.image_path, [self.bbox], 0.9, 0.7)
        if gun_temp is None:
            self.logger.print_log("未找到枪械")
            self.current_gun = None
            return False

        scope_temp, score_scope_temp = self.image_comparator.compare_with_path(self.scope_path, self.scope_bbox, 0.9,
                                                                               0.4)
        if scope_temp is None:
            self.logger.print_log("未找到配件，默认为1倍")
            scope_temp = '1x'

        if gun_temp in self.has_turbocharger:
            hop_up_temp, score_hop_up_temp = self.image_comparator.compare_with_path(self.hop_up_path, self.hop_up_bbox,
                                                                                     0.9, 0.6)
        else:
            hop_up_temp = None
            score_hop_up_temp = 0

        if gun_temp == self.current_gun and scope_temp == self.current_scope and hop_up_temp == self.current_hot_pop:
            self.logger.print_log(
                "当前枪械搭配已经是: {}-{}-{}".format(self.current_gun, self.current_scope, self.current_hot_pop))
            if auto:
                return False
        else:
            self.current_scope = scope_temp
            self.current_gun = gun_temp
            self.current_hot_pop = hop_up_temp
            self.logger.print_log(
                "枪械: {},相似: {}-配件: {},相似: {}-hop_up: {},相似: {}".format(self.current_gun, score_temp,
                                                                                 self.current_scope, score_scope_temp,
                                                                                 self.current_hot_pop,
                                                                                 score_hop_up_temp))

        for func in self.call_back:
            func(self.current_gun, self.current_scope, self.current_hot_pop)
        return True

    def connect(self, func):
        self.call_back.append(func)


class LocalImageComparator(ImageComparator):
    """
        本地图片对比
    """

    def __init__(self, logger: Logger):
        self.image_cache = {}
        self.logger = logger

    def compare_image(self, img, path_image):
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

    def compare_with_path(self, path, bbox_list, lock_score, discard_score):
        """
            截图范围与文件路径内的所有图片对比
        :param path:
        :param bbox_list:
        :param lock_score:
        :param discard_score:
        :return:
        """
        select_name = ''
        score_temp = 0.00000000000000000000
        for scope_bbox_item in bbox_list:
            img = ImageGrab.grab(bbox=scope_bbox_item)
            for fileName in [file for file in os.listdir(path) if file.endswith('.png') or file.endswith(".jpg")]:
                score = self.compare_image(img, path + fileName)
                if score > score_temp:
                    score_temp = score
                    select_name = fileName.split('.')[0]
                if score_temp > lock_score:
                    break
        if score_temp < discard_score:
            select_name = None
        return select_name, score_temp
