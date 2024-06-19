import cv2
import numpy as np

from log.Logger import Logger
from net.socket.NetImageComparator import NetImageComparator


class DynamicSizeImageComparator(NetImageComparator):
    """
        可动态模糊匹配的网络图片对比
    """

    def __init__(self, logger: Logger, base_path):
        super().__init__(logger, base_path)
        self.image_cache = {}
        self.logger = logger
        self.base_path = base_path

    def compare_with_path(self, path, images, lock_score, discard_score):
        path = self.base_path + path
        file_name_list = [path + fileName for fileName in self.read_file_from_url_and_download(path, "list.txt")]
        select_name, score_temp = self.match_template(images, file_name_list, threshold=discard_score)
        if score_temp > discard_score:
            return select_name, score_temp
        return "", 0.00000000000000000000

    def match_template(self, origin_images, match_image_list, threshold=0.8):
        # scales = np.linspace(0.8, 1.2, 3)[::-1]
        scales = [1]
        for scale in scales:
            for match_image in match_image_list:
                downloaded_image = self.get_image_from_cache(match_image)
                downloaded_image.seek(0)
                image_a = cv2.imdecode(np.frombuffer(downloaded_image.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
                downloaded_image.close()
                template_gray = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
                # 获取模板的原始宽高
                template_height, template_width = template_gray.shape[:2]
                for origin_image in origin_images:
                    # 转换为灰度图
                    image_b = np.array(origin_image)
                    image_gray = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
                    resized = cv2.resize(template_gray, (int(template_width * scale), int(template_height * scale)))
                    if resized.shape[0] > image_gray.shape[0] or resized.shape[1] > image_gray.shape[1]:
                        continue

                    result = cv2.matchTemplate(image_gray, resized, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    if max_val > threshold:
                        return "", max_val
        return "", 0.0
