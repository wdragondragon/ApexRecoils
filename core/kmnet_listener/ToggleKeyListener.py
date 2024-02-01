import time

from core.kmnet_listener.KmBoxNetListener import KmBoxNetListener
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover


class ToggleKeyListener:
    """
        监听kmnet 关于辅助开关键的实现
    """

    def __init__(self, logger: Logger, km_box_net_listener: KmBoxNetListener, delayed_activation_key_list,
                 zen_toggle_key, mouse_c1_to_key,
                 mouse_mover: MouseMover, c1_mouse_mover: MouseMover):
        import kmNet
        self.kmNet = kmNet
        self.logger = logger
        self.mouse_mover = mouse_mover
        self.c1_mouse_mover = c1_mouse_mover
        self.km_box_net_listener = km_box_net_listener
        # 自定义按住延迟转换
        self.zen_toggle_key = zen_toggle_key
        self.delayed_activation_key_status_map = {}
        self.delayed_activation_key_list = [(int(key, 16), value) for key, value in delayed_activation_key_list.items()]
        km_box_net_listener.connect(self.delayed_activation)

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


class DelayedActivationKey:
    """
        开关状态
    """

    def __init__(self):
        self.hold_time = time.time()
        self.handle = False
