from core.screentaker.CapScreenTaker import CapScreenTaker
from core.screentaker.LocalMssScreenTaker import LocalMssScreenTaker
from net.socket.SocketScreenTaker import SocketScreenTaker


def get_screen_taker(screen_taker, distributed_param):
    """
        根据配置获取截图器
    """
    if screen_taker == "local":
        return LocalMssScreenTaker()
    elif screen_taker == "distributed":
        return SocketScreenTaker((distributed_param["ip"], distributed_param["port"]))
    elif screen_taker == 'cap':
        return CapScreenTaker()
