import math
import threading
import time

from core.Config import Config
from core.KeyAndMouseListener import KMCallBack, MouseListener
from core.SelectGun import SelectGun
from log import LogFactory
from mouse_mover.MouseMover import MouseMover


class ShakeGun:
    """
        抖枪
    """

    def __init__(self, config: Config,
                 mouse_listener: MouseListener,
                 mouse_mover: MouseMover,
                 select_gun: SelectGun):
        self.logger = LogFactory.getLogger(self.__class__)
        self.mouse_listener = mouse_listener
        self.mouse_mover = mouse_mover
        self.select_gun = select_gun
        self.config = config
        self.in_shake = False
        self.LMD = 3.0
        self.pushDown = 6
        self.shakeNum = 3
        self.ADS = 1.0
        self.Level = 5
        self.Decline = 9
        self.frequency = 11
        # self.shake_range = (6 // (self.LMD * self.ADS)) + self.Level - 2
        self.shake_range = 17
        self.declineRange = (self.Decline + 2) * self.LMD
        self.declineTime = 0
        self.holdShakeTime = 0
        self.lastFreshCasLockTime = time.time()
        self.shake_gun_toggle_button = self.config.shake_gun_toggle_button
        self.shake_gun_trigger_button = self.config.shake_gun_trigger_button

        KMCallBack.connect(KMCallBack("k", self.shake_gun_trigger_button, self.shake_gun_threading))

        for button_list in self.shake_gun_toggle_button:
            for button in button_list:
                KMCallBack.connect(KMCallBack("m", button, self.shake_gun_threading))

    def shake_gun_threading(self, key_type, key, pressed, toggled):
        if self.in_shake:
            return
        threading.Thread(target=self.shake_gun).start()
        self.in_shake = False

    def shake_gun(self):
        if self.in_shake:
            return
        if self.mouse_mover.is_caps_locked() and self.is_press():
            self.in_shake = True
            self.logger.print_log("开始抖枪")
        else:
            return
        self.clear_time()
        while self.mouse_mover.is_caps_locked() and self.in_shake and self.is_press():
            self.rock_shake()
            self.mouse_relative_by_hold_shake_time()
        self.in_shake = False
        self.logger.print_log("结束抖枪")

    def is_press(self):
        # 遍历外层数组，判断与的关系
        and_result = True
        for and_group in self.shake_gun_toggle_button:
            # 遍历内层数组，判断或的关系
            or_result = False
            for or_button in and_group:
                is_button_press = self.mouse_listener.is_press(or_button)
                # 如果有一个按钮被按下，则内层结果为 True
                or_result = or_result or is_button_press
                if or_result:
                    break
            and_result = and_result and or_result
            if not and_result:
                break
        # 如果所有外层结果都为 False，则整体结果为 False
        return and_result

    def rock_shake(self):
        horizontal = self.shake_range
        vertical = self.shake_range + 5
        for _ in range(self.shakeNum):
            self.mouse_mover.move_rp(int(-horizontal), int(-vertical))
            self.better_sleep(self.frequency)
            self.mouse_mover.move_rp(int(horizontal), int(vertical))
            self.better_sleep(self.frequency)
        pass

    def mouse_relative_by_hold_shake_time(self):
        if self.declineTime >= self.declineRange:
            relative_time = math.log(self.holdShakeTime / 100, 2)
            relative_time = max(relative_time, -1)
            relative_time = min(relative_time, 2)
            relative_time = math.floor(relative_time)
            relative_time = 3 - relative_time
            for _ in range(relative_time):
                self.mouse_mover.move_rp(0, self.pushDown)
            self.declineTime = 0

    def clear_time(self):
        self.declineTime = 0
        self.holdShakeTime = 0
        self.lastFreshCasLockTime = time.time()

    def better_sleep(self, t):
        self.declineTime += t
        self.holdShakeTime += t
        time.sleep(t / 1000)
