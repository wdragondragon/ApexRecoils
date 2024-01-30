from core.kmnet_listener.KmBoxNetListener import KmBoxNetListener
import kmNet


class ToggleKeyListener:
    def __init__(self, km_box_net_listener: KmBoxNetListener, toggle_key):
        self.toggle_key = [int(key, 16) for key in toggle_key]
        self.km_box_net_listener = km_box_net_listener
        self.key_status_map = {}
        self.mask_toggle_key()
        km_box_net_listener.connect(self.toggle_change)

    def mask_toggle_key(self):
        kmNet.unmask_all()
        for key in self.toggle_key:
            kmNet.mask_keyboard(key)
            self.key_status_map[key] = ToggleKey()

    def toggle_change(self):
        for key in self.toggle_key:
            hold_status = kmNet.isdown_keyboard(key) == 1
            toggle_key_status = self.key_status_map[key]

            if not toggle_key_status.last_hold_status and hold_status:
                toggle_key_status.toggle()
                if toggle_key_status.toggle_status:
                    kmNet.keydown(key)
                else:
                    kmNet.keyup(key)
            toggle_key_status.hold(hold_status)

    def destory(self):
        kmNet.unmask_all()
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
