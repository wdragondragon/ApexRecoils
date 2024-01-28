from log.Logger import Logger
from net.socket.Server import Server

if __name__ == '__main__':
    logger = Logger()
    server = Server(logger=logger, net_comparator=True)
