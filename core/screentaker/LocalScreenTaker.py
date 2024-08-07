from PIL import ImageGrab

from core.screentaker.ScreenTaker import ScreenTaker
from log import LogFactory


class LocalScreenTaker(ScreenTaker):
    """
        本地截图
    """

    def __init__(self):
        self.logger = LogFactory.getLogger(self.__class__)

    def get_images_from_bbox(self, bbox_list):
        """
        Get images from specified bounding boxes.

        :param bbox_list: List of bounding boxes [(x1, y1, x2, y2), ...]
        :return: Generator yielding images
        """

        try:
            return list(ImageGrab.grab(bbox=bbox) for bbox in bbox_list)
        except Exception as e:
            self.logger.print_log(f"Error in get_images_from_bbox: {e}")
