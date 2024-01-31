import time

from core.kmnet_listener.KmBoxNetListener import KmBoxNetListener
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover


class ToggleKeyListener:

    def __init__(self, logger: Logger, km_box_net_listener: KmBoxNetListener, toggle_key, delayed_activation_key_list,
                 zen_toggle_key,
                 mouse_mover: MouseMover):
        import kmNet
        self.kmNet = kmNet
        self.logger = logger
        self.mouse_mover = mouse_mover
        self.toggle_key = [int(key, 16) for key in toggle_key]
        self.delayed_activation_key_list = [(int(key, 16), value) for key, value in delayed_activation_key_list.items()]
        self.km_box_net_listener = km_box_net_listener
        self.key_status_map = {}
        self.delayed_activation_key_status_map = {}
        self.zen_toggle_key = zen_toggle_key
        self.mask_toggle_key()
        km_box_net_listener.connect(self.delayed_activation)
        km_box_net_listener.connect(self.toggle_change)

    def mask_toggle_key(self):
        self.kmNet.unmask_all()
        for key in self.toggle_key:
            self.kmNet.mask_keyboard(key)
            self.key_status_map[key] = ToggleKey()

    def toggle_change(self):
        for key in self.toggle_key:
            hold_status = self.kmNet.isdown_keyboard(key) == 1
            toggle_key_status = self.key_status_map[key]

            if not toggle_key_status.last_hold_status and hold_status:
                toggle_key_status.toggle()
                if toggle_key_status.toggle_status:
                    self.kmNet.keydown(key)
                else:
                    self.kmNet.keyup(key)
            toggle_key_status.hold(hold_status)

    def delayed_activation(self):
        for key, key_time in self.delayed_activation_key_list:
            hold_status = self.kmNet.isdown_keyboard(key) == 1

            if hold_status:
                if key not in self.delayed_activation_key_status_map:
                    self.delayed_activation_key_status_map[key] = DelayedActivationKey()

                delayed_activation_key_status = self.delayed_activation_key_status_map[key]
                if int((
                               time.time() - delayed_activation_key_status.hold_time) * 1000) > key_time and not delayed_activation_key_status.handle:
                    delayed_activation_key_status.handle = True
                    self.logger.print_log(f"持续按下{key},{key_time}ms，转换器开关按下：[{self.zen_toggle_key}]")
                    # 转换器切换键
                    self.mouse_mover.click_key(int(self.zen_toggle_key, 16))
            else:
                if key in self.delayed_activation_key_status_map:
                    self.delayed_activation_key_status_map.pop(key)

    def destory(self):
        self.kmNet.unmask_all()
        self.key_status_map.clear()


class ToggleKey:
    """
        开关状态
    """

    def __init__(self):
        self.last_hold_status = False
        self.toggle_status = False

    def toggle(self):
        self.toggle_status = not self.toggle_status

    def hold(self, status):
        self.last_hold_status = status


class DelayedActivationKey:
    """
        开关状态
    """

    def __init__(self):
        self.hold_time = time.time()
        self.handle = False
