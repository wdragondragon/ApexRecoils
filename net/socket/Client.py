import pickle  # 用于序列化/反序列化数据
import socket

from net.socket import SocketUtil


class Client:
    """
        识别客户端
    """

    def __init__(self, socket_address):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(socket_address)

    def compare_with_path(self, path, images, lock_score, discard_score):
        """

        :param path:
        :param images:
        :param lock_score:
        :param discard_score:
        :return:
        """
        data = (path, images, lock_score, discard_score)
        data = pickle.dumps(data)
        SocketUtil.send(self.client_socket, data)
        result_data = SocketUtil.recv(self.client_socket)
        result = pickle.loads(result_data)
        return result
