from log import LogFactory
from mouse_mover.MouseMover import MouseMover
from net.socket.Client import Client


class SocketMouseMover(MouseMover):
    def __init__(self, mouse_mover_param, mode="mouse_mover"):
        super().__init__(mouse_mover_param)
        self.logger = LogFactory.getLogger(self.__class__)
        self.mode = mode
        self.client = Client((mouse_mover_param["ip"], mouse_mover_param["port"]), mode)
        self.listener = None
        self.toggle_key_listener = None

    def move_rp(self, x: int, y: int):
        self.client.mouse_mover("move_rp", (x, y))

    def move(self, x: int, y: int):
        self.client.mouse_mover("move", (x, y))

    def left_click(self):
        self.client.mouse_mover("left_click", ())

    def key_down(self, value):
        self.client.mouse_mover("key_down", (value,))

    def key_up(self, value):
        self.client.mouse_mover("key_up", (value,))

    def get_position(self):
        return super().get_position()

    def is_num_locked(self):
        return super().is_num_locked()

    def is_caps_locked(self):
        return super().is_caps_locked()

    def click_key(self, value):
        self.client.mouse_mover("click_key", (value,))

    def destroy(self):
        """
            销毁
        """
        self.listener.stop()
        self.toggle_key_listener.destory()

    def toggle_caps_lock(self, lock_status):
        self.client.mouse_mover("toggle_caps_lock", (lock_status,))

    def mouse_click(self, key, press):
        self.client.mouse_mover("mouse_click", (key, press))
