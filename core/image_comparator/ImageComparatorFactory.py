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
    if comparator_mode == 0:
        return LocalImageComparator(logger, base_path)
    elif comparator_mode == 1:
        return NetImageComparator(logger, base_path)
    elif comparator_mode == 2:
        # return SocketImageComparator(logger, ("1.15.138.227", 12345))
        return SocketImageComparator(logger)
