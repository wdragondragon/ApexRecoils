import os

import cv2
import numpy as np
from skimage.metrics import structural_similarity

from core.image_comparator.ImageComparator import ImageComparator
from log.Logger import Logger


class LocalImageComparator(ImageComparator):
    """
        本地图片对比
    """

    def __init__(self, logger: Logger, base_path):
        self.image_cache = {}
        self.logger = logger
        self.base_path = base_path

    def compare_image(self, img, path_image):
        """
            图片对比
        :param img:
        :param path_image:
        :return:
        """
        image_a = np.array(img)
        image_b = cv2.imdecode(np.fromfile(path_image, dtype=np.uint8), cv2.IMREAD_COLOR)
        gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        (score, diff) = structural_similarity(gray_a, gray_b, full=True)
        return score

    def compare_with_path(self, path, images, lock_score, discard_score):
        """
            截图范围与文件路径内的所有图片对比
        :param path:
        :param images:
        :param lock_score:
        :param discard_score:
        :return:
        """
        path = self.base_path + path
        select_name = ''
        score_temp = 0.00000000000000000000
        for img in images:
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
