from core.screentaker.ScreenTaker import ScreenTaker
from log import LogFactory
from net.socket.Client import Client


class SocketScreenTaker(ScreenTaker):
    """
        网络截图
    """

    def __init__(self, socket_address=("127.0.0.1", 12345)):
        self.logger = LogFactory.getLogger(self.__class__)
        self.client = Client(socket_address, "screen_taker")

    def get_images_from_bbox(self, bbox_list):
        return self.client.get_images_from_bbox(bbox_list)
