from tools.Tools import Tools
from log.Logger import Logger


class KeyListener:
    """
        键盘监听器
    """

    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.press_key = dict()
        self.toggle_key_map = []

    def on_press(self, key):
        """
            键盘按下事件
        :param key:
        """
        key_name = self.get_key_name(key)

        if key_name is not None:
            self.press_key[key_name] = Tools.current_milli_time()

        if key_name in self.toggle_key_map:
            self.toggle_key_map.remove(key_name)
        else:
            self.toggle_key_map.append(key_name)
        for cb in KMCallBack.toggle_call_back:
            if cb.key_type == 'k' and cb.key == key_name and cb.is_press:
                cb.call_back(cb.key_type, cb.key, True, cb.key in self.toggle_key_map)

    # 释放按钮，按esc按键会退出监听
    def on_release(self, key):
        """
            键盘释放事件
        :param key:
        """
        key_name = self.get_key_name(key)
        if key_name is not None and key_name in self.press_key:
            self.press_key.pop(key_name)
        for cb in KMCallBack.toggle_call_back:
            if cb.key_type == 'k' and cb.key == key_name and not cb.is_press:
                cb.call_back(cb.key_type, cb.key, True, cb.key in self.toggle_key_map)

    def is_open(self, button):
        """
            判断按钮作为开关的开关状态
        :param button:
        :return:
        """
        return button in self.press_key

    def get_key_name(self, key):
        """
            从key中获取key_name
        :param key:
        :return:
        """
        key_name = None
        if not hasattr(key, 'name') and hasattr(key, 'char') and key.char is not None:
            key_name = key.char
        elif hasattr(key, 'name') and key.name is not None:
            key_name = key.name
        return key_name


class MouseListener:
    """
        鼠标监听器
    """

    def __init__(self, logger: Logger):
        super().__init__()
        self.logger = logger
        self.on_mouse_key_map = dict()
        self.toggle_mouse_key_map = []

    def on_move(self, x, y):
        """
            鼠标移动监听
        :param x:
        :param y:
        """
        pass

    def on_click(self, x, y, button, pressed):
        """
            鼠标按下释放监听
        :param x:
        :param y:
        :param button:
        :param pressed:`
        :return:
        """
        if pressed:
            if button in self.on_mouse_key_map:
                return
            self.on_mouse_key_map[button] = Tools.current_milli_time()
            if button.name in self.toggle_mouse_key_map:
                self.toggle_mouse_key_map.remove(button.name)
            else:
                self.toggle_mouse_key_map.append(button.name)
            for cb in KMCallBack.toggle_call_back:
                if cb.key_type == 'm' and cb.key == button.name and cb.is_press:
                    cb.call_back(cb.key_type, cb.key, pressed, cb.key in self.toggle_mouse_key_map)
        elif not pressed:
            if button not in self.on_mouse_key_map:
                return
            self.on_mouse_key_map.pop(button)
            for cb in KMCallBack.toggle_call_back:
                if cb.key_type == 'm' and cb.key == button.name and not cb.is_press:
                    cb.call_back(cb.key_type, cb.key, pressed, cb.key in self.toggle_mouse_key_map)

    def on_scroll(self, x, y, dx, dy):
        """
            鼠标滚轮监听
        :param x:
        :param y:
        :param dx:
        :param dy:
        """
        pass

    def is_press(self, button):
        """
            判断鼠标是否处于按下状态
        :param button:
        :return:
        """
        return button in self.on_mouse_key_map

    def is_toggle(self, button):
        """
            判断鼠标按键作为开关时的开关状态
        :param button:
        :return:
        """
        return button.name in self.toggle_mouse_key_map

    def press_time(self, button):
        """
            获取鼠标按下时长
        :param button:
        :return:
        """
        if self.is_press(button):
            return Tools.current_milli_time() - self.on_mouse_key_map[button]
        else:
            return 0


class KMCallBack:
    """
        注册键盘或鼠标回调事件
    """
    toggle_call_back = []

    def __init__(self, key_type, key, call_back, is_press=True):
        super().__init__()
        self.key_type = key_type
        self.key = key
        self.call_back = call_back
        self.is_press = is_press

    @staticmethod
    def connect(callback):
        """
            注册事件
        :param callback:
        """
        KMCallBack.toggle_call_back.append(callback)

    @staticmethod
    def remove(key_type, key, is_press=True):
        """
            移除事件
        :param key_type:
        :param key:
        :param is_press:
        """
        remove_cb = []
        for cb in KMCallBack.toggle_call_back:
            if cb.key_type == key_type and cb.key == key and cb.is_press == is_press:
                remove_cb.append(cb)
        for cb in remove_cb:
            KMCallBack.toggle_call_back.remove(cb)
