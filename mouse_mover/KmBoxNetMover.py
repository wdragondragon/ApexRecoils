import kmNet

from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover


class KmBoxNetMover(MouseMover):

    def __init__(self, logger: Logger, mouse_mover_param):
        # 初始化
        super().__init__(mouse_mover_param)
        self.logger = logger
        ip = mouse_mover_param["ip"]
        port = mouse_mover_param["port"]
        uuid = mouse_mover_param["uuid"]
        kmNet.init(ip, port, uuid)  # 连接盒子
        self.listener = None

    def left_click(self):
        # 左键
        self.left(1)
        self.left(0)

    def left(self, vk_key: int):
        """
            鼠标左键控制 0松开 1按下
        """
        # 左键
        kmNet.left(1)
        kmNet.left(0)

    def move_rp(self, short_x: int, short_y: int, re_cut_size=0):
        kmNet.move(short_x, short_y)

    def move(self, short_x: int, short_y: int):
        """
        鼠标相对移动
        x		:鼠标X轴方向移动距离
        y		:鼠标Y轴方向移动距离
        返回值：
                -1：发送失败\n
                0：发送成功\n
        """

        kmNet.move_auto(short_x, short_y, int(max(5, short_x / 10, short_y / 10)))

    def destroy(self):
        """
            销毁
        """
        self.listener.stop()

    def click_key(self, value):
        kmNet.keydown(value)
        kmNet.keyup(value)