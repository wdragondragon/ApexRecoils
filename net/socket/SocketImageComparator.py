from core.ImageComparator import ImageComparator
from log.Logger import Logger
from net.socket.Client import Client


class SocketImageComparator(ImageComparator):
    def __init__(self, logger: Logger):
        # 用于缓存已下载图像的字典
        self.image_cache = {}
        self.logger = logger
        self.client = Client("127.0.0.1", 12345)

    def compare_with_path(self, path, images, lock_score, discard_score):
        """
            截图范围与文件路径内的所有图片对比
        :param path:
        :param images:
        :param lock_score:
        :param discard_score:
        :return:
        """
        return self.client.compare_with_path(path, images, lock_score, discard_score)
