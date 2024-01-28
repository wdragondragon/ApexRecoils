from log.Logger import Logger
from net.socket.Server import Server

if __name__ == '__main__':
    logger = Logger()
    server = Server(logger=logger, server_address=("127.0.0.1", 12345), net_comparator=True)
