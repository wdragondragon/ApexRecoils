from core.screentaker.LocalMssScreenTaker import LocalMssScreenTaker
from net.socket.SocketScreenTaker import SocketScreenTaker


def get_screen_taker(logger, screen_taker, distributed_param):
    """
        根据配置获取截图器
    """
    if screen_taker == "local":
        return LocalMssScreenTaker(logger)
    elif screen_taker == "distributed":
        return SocketScreenTaker(logger, (distributed_param["ip"], distributed_param["port"]))
