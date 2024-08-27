from core.screentaker.CapScreenTaker import CapScreenTaker
from core.screentaker.LocalMssScreenTaker import LocalMssScreenTaker
from net.socket.SocketScreenTaker import SocketScreenTaker


def get_screen_taker(config):
    """
        根据配置获取截图器
    """
    screen_taker = config.screen_taker
    if screen_taker == "local":
        return LocalMssScreenTaker()
    elif screen_taker == "distributed":
        return SocketScreenTaker((config.distributed_param["ip"], config.distributed_param["port"]))
    elif screen_taker == 'cap':
        return CapScreenTaker(config.cap_param)
