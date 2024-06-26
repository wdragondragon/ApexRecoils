from core.image_comparator.LocalImageComparator import LocalImageComparator
from net.socket.NetImageComparator import NetImageComparator
from net.socket.SocketImageComparator import SocketImageComparator


def get_image_comparator(comparator_mode, config):
    """
        获取图片对比器
    :param config:
    :param comparator_mode:
    :param logger:
    :return:
    """
    if comparator_mode == "local":
        return LocalImageComparator(config.image_base_path)
    elif comparator_mode == "net":
        return NetImageComparator(config.image_base_path)
    elif comparator_mode == "distributed":
        # return SocketImageComparator(logger, ("1.15.138.227", 12345))
        return SocketImageComparator((config.distributed_param["ip"], config.distributed_param["port"]))
