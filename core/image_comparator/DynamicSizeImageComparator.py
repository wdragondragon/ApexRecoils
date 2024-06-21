import cv2
import numpy as np
from skimage.metrics import structural_similarity

from log.Logger import Logger
from net.socket.NetImageComparator import NetImageComparator


class DynamicSizeImageComparator(NetImageComparator):
    """
        可动态模糊匹配的网络图片对比
    """

    def __init__(self, logger: Logger, base_path, screen_taker):
        super().__init__(logger, base_path)
        self.image_cache = {}
        self.logger = logger
        self.base_path = base_path
        self.screen_taker = screen_taker

    def compare_with_path(self, path, images, lock_score, discard_score):
        path = self.base_path + path
        image_info_arr = [image_info.split() for image_info in
                          self.read_file_from_url(path + "list.txt")]
        select_name, score_temp = self.match_template(path, image_info_arr, threshold=discard_score)
        return select_name, score_temp

    def match_template(self, path, image_info_arr, threshold=0.8):
        for image_info in image_info_arr:
            file_path = path + image_info[0]
            box = (int(image_info[1]), int(image_info[2]), int(image_info[3]), int(image_info[4]))
            downloaded_image = self.get_image_from_cache(file_path)
            downloaded_image.seek(0)
            image_a = cv2.imdecode(np.frombuffer(downloaded_image.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
            downloaded_image.close()
            image_b = self.screen_taker.get_images_from_bbox([box])[0]
            image_b = np.array(image_b)
            gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
            gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

            (score, diff) = structural_similarity(gray_a, gray_b, full=True)
            if score > threshold:
                return image_info[0], score
        return "", 0.0
