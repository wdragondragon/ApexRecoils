from core.image_comparator.ImageComparator import ImageComparator
from log import LogFactory
from net.socket.Client import Client


class SocketImageComparator(ImageComparator):
    def __init__(self, base_path, socket_address=("127.0.0.1", 12345)):
        # 用于缓存已下载图像的字典
        super().__init__(base_path)
        self.image_cache = {}
        self.logger = LogFactory.getLogger(self.__class__)
        self.client = Client(socket_address, "compare_with_path")

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
