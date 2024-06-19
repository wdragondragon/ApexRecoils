import threading
import time

import pygame

from core.image_comparator.DynamicSizeImageComparator import DynamicSizeImageComparator
from core.joy_listener.JoyListener import JoyListener
from core.screentaker.ScreenTaker import ScreenTaker
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover


class S1SwitchMonitor:
    def __init__(self, logger: Logger, joy_listener: JoyListener,
                 licking_state_path,
                 licking_state_bbox,
                 toggle_key,
                 dynamicSizeImageComparator: DynamicSizeImageComparator,
                 screen_taker: ScreenTaker,
                 mouser_mover: MouseMover, retry=5):
        self.logger = logger
        self.dynamicSizeImageComparator = dynamicSizeImageComparator
        self.licking_state_path = licking_state_path
        self.licking_state_bbox = licking_state_bbox
        self.toggle_key = toggle_key
        self.screen_taker = screen_taker
        self.mouser_mover = mouser_mover
        self.click_state = False
        self.threading_state = False
        self.retry = retry
        # todo 添加监听手柄按键类型
        joy_listener.connect_joystick(pygame.JOYAXISMOTION, self.monitor)

    def monitor(self):
        if not self.threading_state:
            self.threading_state = True
            threading.Thread(target=self.monitor_thread).start()

    def monitor_thread(self):
        # todo 需要添加监听手柄舔包键长按之后触发识别
        retry = 0
        # 触发后背包判断后，开始识别，识别到背包中则按下切层，直到未识别到背包则松开并退出循环
        while True:
            images = self.screen_taker.get_images_from_bbox(self.licking_state_bbox)
            _, score = self.dynamicSizeImageComparator.compare_with_path(path=self.licking_state_path, images=images,
                                                                         lock_score=1,
                                                                         discard_score=0.6)

            if not self.click_state:
                if score > 0.0:
                    self.click_state = True
                    self.mouser_mover.key_down(self.toggle_key)
                    self.logger.print_log("按下舔包键")
                else:
                    retry += 1
                    if retry == self.retry:
                        break
            elif self.click_state and score <= 0.0:
                self.click_state = False
                self.mouser_mover.key_up(self.toggle_key)
                self.logger.print_log("松开舔包键")
                break
            time.sleep(0.2)
        self.threading_state = False
