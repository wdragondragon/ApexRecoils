import socket
import traceback
import numpy as np
from log.Logger import Logger
from net.socket import SocketUtil


class Server:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.server_socket = None
        self.buffer_size = 4096
        self.open()
        self.listen()

    def open(self):
        # 创建一个TCP/IP套接字
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定服务器地址和端口
        server_address = ("127.0.0.1", 12345)
        self.server_socket.bind(server_address)
        # 监听客户端连接
        self.server_socket.listen(1)

    def listen(self):
        while True:
            self.logger.print_log('等待客户端连接...')
            # 等待客户端连接
            client_socket, client_address = self.server_socket.accept()
            self.logger.print_log('客户端已连接:{}'.format(client_address))
            try:
                img_data = SocketUtil.recv(client_socket, buffer_size=self.buffer_size)
                img0 = np.frombuffer(img_data, dtype='uint8')
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
