import time

from pynput.mouse import Button



from mouse_mover.KmBoxNetMover import KmBoxNetMover


class KmBoxNetListener:
    def __init__(self, km_box_net_mover: KmBoxNetMover, mouse_listener):
        import kmNet
        self.kmNet = kmNet
        self.mouse_listener = mouse_listener
        self.km_box_net_mover = km_box_net_mover
        self.listener_sign = False
        self.down_key_map = []
        self.down_mouse_map = []
        self.connect_func = []
        kmNet.monitor(10000)
        # kmNet.unmask_all()
        # kmNet.mask_keyboard(0x06)

    def km_box_net_start(self):
        self.listener_sign = True
        print("km box net 监听启动")
        while self.listener_sign:
            if self.kmNet.isdown_left():
                if "left" not in self.down_mouse_map:
                    self.down_mouse_map.append("left")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.left, True)
            else:
                if "left" in self.down_mouse_map:
                    self.down_mouse_map.remove("left")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.left, False)

            if self.kmNet.isdown_right():
                if "right" not in self.down_mouse_map:
                    self.down_mouse_map.append("right")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.right, True)
            else:
                if "right" in self.down_mouse_map:
                    self.down_mouse_map.remove("right")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.right, False)

            if self.kmNet.isdown_middle():
                if "middle" not in self.down_mouse_map:
                    self.down_mouse_map.append("middle")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.middle, True)
            else:
                if "middle" in self.down_mouse_map:
                    self.down_mouse_map.remove("middle")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.middle, False)

            if self.kmNet.isdown_side1():
                if "x1" not in self.down_mouse_map:
                    self.down_mouse_map.append("x1")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x1, True)

            else:
                if "x1" in self.down_mouse_map:
                    self.down_mouse_map.remove("x1")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x1, False)
            if self.kmNet.isdown_side2():
                if "x2" not in self.down_mouse_map:
                    self.down_mouse_map.append("x2")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x2, True)
            else:
                if "x2" in self.down_mouse_map:
                    self.down_mouse_map.remove("x2")
                    self.mouse_listener.on_click(*self.km_box_net_mover.get_position(), Button.x2, False)
            for func in self.connect_func:
                func()
            time.sleep(0.01)
        print("km box net 监听结束")

    def stop(self):
        self.listener_sign = False
        self.connect_func.clear()

    def connect(self, func):
        self.connect_func.append(func)
