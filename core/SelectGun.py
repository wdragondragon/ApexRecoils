import os

from PIL import ImageGrab

from core.KeyAndMouseListener import KMCallBack
from tools.Tools import Tools
from log.Logger import Logger


class SelectGun:
    """
        枪械识别
    """

    def __init__(self, logger: Logger, bbox, image_path, refresh_buttons):
        super().__init__()
        self.logger = logger
        self.on_key_map = dict()
        self.bbox = bbox
        self.image_path = image_path
        self.select_gun_sign = False
        self.current_gun = None
        self.refresh_buttons = refresh_buttons
        for refresh_button in self.refresh_buttons:
            KMCallBack.connect(KMCallBack("k", refresh_button, self.select_gun, False))

    def select_gun(self, pressed=False, toggle=False):
        """
            使用图片对比，逐一识别枪械，相似度最高设置为current_gun
        :return:
        """
        if self.select_gun_sign:
            return
        self.select_gun_sign = True
        score_temp = 0.00000000000000000000
        img = ImageGrab.grab(bbox=self.bbox)
        gun_temp = ''
        for fileName in os.listdir(self.image_path):
            score = Tools.compare_image(img, self.image_path + fileName)
            if score > score_temp:
                score_temp = score
                gun_temp = fileName.split('.')[0]
            if score_temp > 0.9:
                break
        if score_temp < 0.7:
            self.logger.print_log("未找到枪械")
            self.current_gun = None
            self.select_gun_sign = False
            return
        if gun_temp == self.current_gun:
            self.logger.print_log("当前枪械已经是: {}".format(self.current_gun))
            self.select_gun_sign = False
            return
        self.current_gun = gun_temp
        self.logger.print_log("枪械: {}, 最大相似度: {}".format(self.current_gun, score_temp))
        self.select_gun_sign = False
