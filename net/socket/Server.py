import pickle
import socket
import traceback

from core.image_comparator.LocalImageComparator import LocalImageComparator
from log.Logger import Logger
from net.socket import SocketUtil
from net.socket.NetImageComparator import NetImageComparator


class Server:
    """
        识别服务端
    """

    def __init__(self, logger: Logger, server_address, net_comparator):
        self.logger = logger
        self.server_address = server_address
        if net_comparator:
            self.image_comparator = NetImageComparator(logger)
        else:
            self.image_comparator = LocalImageComparator(logger)
        self.server_socket = None
        self.buffer_size = 4096
        self.open()
        self.listen()

    def open(self):
        """
            打开服务端
        """
        # 创建一个TCP/IP套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定服务器地址和端口
        self.server_socket.bind(self.server_address)
        # 监听客户端连接
        self.server_socket.listen(1)

    def listen(self):
        """
            监听
        """
        while True:
            self.logger.print_log('等待客户端连接...')
            # 等待客户端连接
            client_socket, client_address = self.server_socket.accept()
            self.logger.print_log('客户端已连接:{}'.format(client_address))
            try:
                while True:
                    data = SocketUtil.recv(client_socket)
                    data = pickle.loads(data)
                    result = self.image_comparator.compare_with_path(*data)
                    result_data = pickle.dumps(result)
                    SocketUtil.send(client_socket, result_data)
            except Exception as e:
                print(e)
                traceback.print_exc()
            finally:
                # 关闭连接
                try:
                    client_socket.close()
                except Exception as e:
                    print(e)
                    traceback.print_exc()
