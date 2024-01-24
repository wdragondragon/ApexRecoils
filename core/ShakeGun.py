import math
import threading
import time

from pynput.mouse import Button

from core.KeyAndMouseListener import KMCallBack, MouseListener
from core.SelectGun import SelectGun
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover


class ShakeGun:
    """
        抖枪
    """

    def __init__(self, logger: Logger,
                 mouse_listener: MouseListener,
                 mouse_mover: MouseMover,
                 select_gun: SelectGun):
        self.logger = logger
        self.mouse_listener = mouse_listener
        self.mouse_mover = mouse_mover
        self.select_gun = select_gun
        self.in_shake = False
        self.LMD = 3.0
        self.pushDown = 1
        self.shakeNum = 1
        self.ADS = 1.0
        self.Level = 5
        self.Decline = 5
        self.frequency = 4
        self.shake_range = (6 // (self.LMD * self.ADS)) + self.Level - 2
        self.declineRange = (self.Decline + 2) * self.LMD
        self.declineTime = 0
        self.holdShakeTime = 0
        self.lastFreshCasLockTime = time.time()
        KMCallBack.connect(KMCallBack("m", 'left', self.shake_gun_threading))
        KMCallBack.connect(KMCallBack("m", 'right', self.shake_gun_threading))
        KMCallBack.connect(KMCallBack("k", 'caps_lock', self.shake_gun_threading))

    def shake_gun_threading(self, pressed, toggled):
        if self.in_shake:
            return
        threading.Thread(target=self.shake_gun).start()
        self.in_shake = False

    def shake_gun(self):
        if self.in_shake:
            return
        if self.mouse_listener.is_press(Button.left) and self.mouse_listener.is_press(
                Button.right) and self.mouse_mover.is_caps_locked():
            self.in_shake = True
            self.logger.print_log("开始抖枪")
        else:
            return
        self.clear_time()
        while self.mouse_listener.is_press(Button.left) and self.mouse_listener.is_press(
                Button.right) and self.mouse_mover.is_caps_locked() and self.in_shake:
            self.rock_shake()
            self.mouse_relative_by_hold_shake_time()
        self.in_shake = False
        self.logger.print_log("结束抖枪")

    def rock_shake(self):
        horizontal = self.shake_range
        vertical = self.shake_range
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
