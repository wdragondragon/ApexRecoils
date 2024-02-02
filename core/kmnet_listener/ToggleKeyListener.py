import time

from core.kmnet_listener.KmBoxNetListener import KmBoxNetListener
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover
from tools.Tools import Tools


class ToggleKeyListener:
    """
        监听kmnet 关于辅助开关键的实现
    """

    def __init__(self, logger: Logger, km_box_net_listener: KmBoxNetListener, delayed_activation_key_list,
                 zen_toggle_key,
                 mouse_mover: MouseMover, c1_mouse_mover: MouseMover, toggle_hold_key):
        import kmNet
        self.kmNet = kmNet
        self.logger = logger
        self.mouse_mover = mouse_mover
        self.c1_mouse_mover = c1_mouse_mover
        self.km_box_net_listener = km_box_net_listener
        # 自定义按住延迟转换
        self.zen_toggle_key = zen_toggle_key
        self.delayed_activation_key_status_map = {}
        self.delayed_activation_key_list = [(Tools.convert_to_decimal(key), value) for key, value in
                                            delayed_activation_key_list.items()]
        km_box_net_listener.connect(self.delayed_activation)

        # 自定义切换按住键
        self.key_status_map = {}
        self.toggle_hold_key = toggle_hold_key
        self.toggle_close_key = {}

        for key in self.toggle_hold_key:
            close_keys = self.toggle_hold_key[key]
            for close_key in close_keys:
                if close_key not in self.toggle_close_key:
                    self.toggle_close_key[close_key] = []
                if Tools.convert_to_decimal(key) is None:
                    continue
                self.toggle_close_key[close_key].append(key)

        self.mask_toggle_key()
        km_box_net_listener.connect(self.toggle_change)

    def mask_toggle_key(self):
        self.kmNet.unmask_all()
        for key in self.toggle_hold_key:
            self.kmNet.mask_keyboard(Tools.convert_to_decimal(key))
            self.key_status_map[key] = ToggleKey()

    def toggle_change(self):
        for key in self.toggle_hold_key:
            num_key = Tools.convert_to_decimal(key)
            if num_key is None:
                continue
            hold_status = self.kmNet.isdown_keyboard(num_key) == 1
            toggle_key_status = self.key_status_map[key]

            if not toggle_key_status.last_hold_status and hold_status:
                toggle_key_status.toggle()
                if toggle_key_status.toggle_status:
                    self.logger.print_log(f"启动长按" + key)
                    self.mouse_mover.key_down(num_key)
                else:
                    self.logger.print_log(f"关闭长按" + key)
                    self.mouse_mover.key_up(num_key)
            toggle_key_status.hold(hold_status)

        for close_key in self.toggle_close_key:
            num_close_key = Tools.convert_to_decimal(close_key)
            if num_close_key is None:
                continue
            hold_status = self.kmNet.isdown_keyboard(num_close_key) == 1
            if not hold_status:
                continue
            keys = self.toggle_close_key[close_key]
            for key in keys:
                if key not in self.key_status_map:
                    continue
                toggle_key_status = self.key_status_map[key]
                if toggle_key_status.toggle_status:
                    self.logger.print_log(f"关闭长按" + key)
                    self.mouse_mover.key_up(Tools.convert_to_decimal(key))
                    toggle_key_status.toggle()

    def controller_toggle_hold_change(self, key):
        if key in self.toggle_close_key:
            keys = self.toggle_close_key[key]
            for key in keys:
                if key not in self.key_status_map:
                    continue
                toggle_key_status = self.key_status_map[key]
                if toggle_key_status.toggle_status:
                    self.logger.print_log(f"关闭长按" + key)
                    self.mouse_mover.key_up(Tools.convert_to_decimal(key))
                    toggle_key_status.toggle()

    def delayed_activation(self):
        for key, delayed_param in self.delayed_activation_key_list:
            key_time = delayed_param["delay"]
            deactivation = delayed_param["up_deactivation"]
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
                    self.mouse_mover.click_key(Tools.convert_to_decimal(self.zen_toggle_key))
            else:
                if key in self.delayed_activation_key_status_map:
                    # 转换器切换键
                    if deactivation and key in self.delayed_activation_key_status_map and \
                            self.delayed_activation_key_status_map[key].handle:
                        self.logger.print_log(f"持续按下{key}后弹起，转换器开关按下：[{self.zen_toggle_key}]")
                        self.mouse_mover.click_key(Tools.convert_to_decimal(self.zen_toggle_key))
                    self.delayed_activation_key_status_map.pop(key)

    def destory(self):
        self.kmNet.unmask_all()


class DelayedActivationKey:
    """
        开关状态
    """

    def __init__(self):
        self.hold_time = time.time()
        self.handle = False


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
