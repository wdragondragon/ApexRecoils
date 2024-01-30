from core.image_comparator.LocalImageComparator import LocalImageComparator
from net.socket.NetImageComparator import NetImageComparator
from net.socket.SocketImageComparator import SocketImageComparator


def get_image_comparator(comparator_mode, logger, base_path):
    """
        获取图片对比器
    :param base_path:
    :param comparator_mode:
    :param logger:
    :return:
    """
    if comparator_mode == "local":
        return LocalImageComparator(logger, base_path)
    elif comparator_mode == "net":
        return NetImageComparator(logger, base_path)
    elif comparator_mode == "distributed":
        # return SocketImageComparator(logger, ("1.15.138.227", 12345))
        return SocketImageComparator(logger)
