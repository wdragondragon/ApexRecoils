from core.screentaker.ScreenTaker import ScreenTaker
from log.Logger import Logger
from net.socket.Client import Client


class SocketScreenTaker(ScreenTaker):
    """
        网络截图
    """

    def __init__(self, logger: Logger, socket_address=("127.0.0.1", 12345)):
        self.logger = logger
        self.client = Client(socket_address, "screen_taker")

    def get_images_from_bbox(self, bbox_list):
        return self.client.get_images_from_bbox(bbox_list)
