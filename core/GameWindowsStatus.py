import threading
import time

from log import LogFactory
from tools.Tools import Tools


class GameWindowsStatus:
    """
        游戏窗口状态检测
    """

    def __init__(self):
        self.status = False
        self.logger = LogFactory.getLogger(self.__class__)
        self.timing_get_status_thread()

    def timing_get_status_thread(self):
        """
            新线程检测
        """
        threading.Thread(target=self.timing_get_status).start()

    def timing_get_status(self):
        """
            检测窗口
        """
        while True:
            status = Tools.is_apex_windows()
            if self.status != status:
                self.status = status
                self.logger.print_log(f"窗口状态切换{self.status}")
            time.sleep(2)

    def get_game_windows_status(self):
        """
            获取状态
        """
        return self.status
