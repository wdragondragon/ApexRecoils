from core.screentaker.LocalScreenTaker import LocalScreenTaker
from net.socket.SocketScreenTaker import SocketScreenTaker


def get_screen_taker(logger, config):
    """
        根据配置获取截图器
    """
    screen_taker = config.screen_taker
    if screen_taker == "local":
        return LocalScreenTaker(logger)
    elif screen_taker == "distributed":
        return SocketScreenTaker(logger, (config.distributed_param["ip"], config.distributed_param["port"]))
