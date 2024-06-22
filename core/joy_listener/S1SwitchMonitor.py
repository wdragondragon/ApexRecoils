import threading
import time

import pygame

from core.image_comparator.DynamicSizeImageComparator import DynamicSizeImageComparator
from core.joy_listener.JoyListener import JoyListener
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover
from tools.Tools import Tools


class S1SwitchMonitor:
    def __init__(self, logger: Logger, joy_listener: JoyListener,
                 licking_state_path,
                 licking_state_bbox,
                 dynamic_size_image_comparator: DynamicSizeImageComparator,
                 mouser_mover: MouseMover, s1_switch_hold_map, retry=5):
        self.logger = logger
        self.dynamic_size_image_comparator = dynamic_size_image_comparator
        self.licking_state_path = licking_state_path
        self.licking_state_bbox = licking_state_bbox
        self.mouser_mover = mouser_mover
        self.click_state = False
        self.threading_state = False
        self.retry = retry
        self.dict = {
            pygame.JOYBUTTONDOWN: "JOYBUTTONDOWN",
            pygame.JOYBUTTONUP: "JOYBUTTONUP"
        }
        self.s1_switch_hold_map = s1_switch_hold_map
        self.hold_key = self.s1_switch_hold_map["key"]
        self.toggle_key = self.s1_switch_hold_map["toggle_key"]
        self.hole_key_status_map = {}
        # todo 添加监听手柄按键类型
        joy_listener.connect_joystick(pygame.JOYBUTTONUP, self.monitor)
        joy_listener.connect_joystick(pygame.JOYBUTTONDOWN, self.monitor)

    def monitor(self, joystick, event):
        if event.type in self.dict:
            if event.type == pygame.JOYBUTTONDOWN and event.button not in self.hole_key_status_map:
                self.hole_key_status_map[event.button] = time.time()
            elif event.type == pygame.JOYBUTTONUP and event.button in self.hole_key_status_map:
                self.hole_key_status_map.pop(event.button)
            if str(event.button) in self.hold_key and not self.threading_state:
                self.threading_state = True
                threading.Thread(target=self.monitor_thread, args=(joystick,)).start()

    def monitor_thread(self, joystick):
        # todo 需要添加监听手柄舔包键长按之后触发识别
        retry = 0
        # 触发后背包判断后，开始识别，识别到背包中则按下切层，直到未识别到背包则松开并退出循环
        # start = time.time()
        detect_time = None
        skip_detect = False
        skip_delay = 0
        while True:
            for key in self.hold_key:
                if int(key) in self.hole_key_status_map.keys():
                    start_time = self.hole_key_status_map[int(key)]
                    delay = self.hold_key[key]["delay"]

                    if self.time_out(start_time, delay):
                        detect_time = self.hold_key[key]["detect_time"]
                        skip_detect = self.hold_key[key]["skip_detect"]
                        if skip_detect:
                            skip_delay = self.hold_key[key]["skip_delay"]
                        self.logger.print_log(f"按下{key}超过{delay}ms，开始识别{detect_time}ms")
                        break
            if detect_time is not None:
                break
            time.sleep(0.001)

        start_time = time.time()
        detect_status = False
        if skip_delay > 0:
            time.sleep(skip_delay / 1000.0)

        while True:
            if not skip_detect or (skip_detect and self.click_state):
                select_name, score = self.dynamic_size_image_comparator.compare_with_path(path=self.licking_state_path,
                                                                                          images=None,
                                                                                          lock_score=1,
                                                                                          discard_score=0.6)
                if score > 0.0:
                    detect_status = True
            else:
                select_name, score = "default", 1

            if not self.click_state:
                if score > 0.0:
                    self.click_state = True
                    self.mouser_mover.key_down(Tools.convert_to_decimal(self.toggle_key))
                    self.logger.print_log(f"按下舔包键:{self.toggle_key}")
                else:
                    retry += 1
                    self.logger.print_log(f"未识别到，重试:{retry}")
                    if self.time_out(start_time, detect_time):
                        break
            elif self.click_state and score <= 0.0:
                if not skip_detect or (skip_detect and (detect_status or self.time_out(start_time, detect_time))):
                    self.click_state = False
                    self.mouser_mover.key_up(Tools.convert_to_decimal(self.toggle_key))
                    self.logger.print_log(f"松开舔包键:{self.toggle_key}")
                    break
                else:
                    retry += 1
                    self.logger.print_log(f"未识别到，重试:{retry}")

        self.threading_state = False

    def time_out(self, start_time, detect_time):
        return int((time.time() - start_time) * 1000) > detect_time
