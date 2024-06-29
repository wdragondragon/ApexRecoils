import threading
import time
import traceback

from core.KeyAndMouseListener import KMCallBack
from core.screentaker.ScreenTaker import ScreenTaker
from log import LogFactory


class SelectGun:
    """
        枪械识别
    """

    def __init__(self, bbox, image_path, scope_bbox, scope_path, hop_up_bbox, hop_up_path,
                 refresh_buttons, has_turbocharger, image_comparator, screen_taker: ScreenTaker, game_windows_status,
                 delay_refresh_buttons=None):
        super().__init__()
        self.logger = LogFactory.getLogger(self.__class__)
        self.on_key_map = dict()
        self.bbox = bbox
        self.image_path = image_path
        self.scope_bbox = scope_bbox
        self.scope_path = scope_path
        self.select_gun_sign = True
        self.current_gun = None
        self.current_scope = None
        self.current_hot_pop = None
        self.refresh_buttons = refresh_buttons
        self.has_turbocharger = has_turbocharger
        self.hop_up_bbox = hop_up_bbox
        self.hop_up_path = hop_up_path
        self.call_back = []
        self.fail_time = 0
        self.image_comparator = image_comparator
        self.screen_taker = screen_taker
        self.game_windows_status = game_windows_status
        self.select_gun_cache = {}

        for refresh_button in self.refresh_buttons:
            KMCallBack.connect(KMCallBack("k", refresh_button, self.select_gun_threading, False))

        if delay_refresh_buttons is None:
            delay_refresh_buttons = {}
        self.delay_refresh_buttons = delay_refresh_buttons
        self.delay_refresh_buttons_map = {}
        for refresh_button, delay in self.delay_refresh_buttons.items():
            self.delay_refresh_buttons_map[refresh_button] = delay
            KMCallBack.connect(KMCallBack("k", refresh_button, self.select_gun_threading, False))

        threading.Thread(target=self.timing_execution).start()

    def timing_execution(self):
        """
            定时识别
        """
        while True:
            try:
                if self.game_windows_status.get_game_windows_status():
                    self.logger.print_log("定时识别开始")
                    if self.select_gun_with_sign(None, None, auto=True):
                        self.fail_time = 0
                    else:
                        self.fail_time += 1
                    self.logger.print_log(f"下一轮定时识别在[{1 + self.fail_time / 5}]秒后")
                else:
                    self.fail_time = 0
            except Exception as e:
                traceback.print_exc()
                pass
            time.sleep(1 + self.fail_time / 5)

    def select_gun_threading(self, key_type, key, pressed=False, toggle=False):
        """

        :param pressed:
        :param toggle:
        :param key_type:
        :param key:
        :return:
        """
        if self.select_gun_sign:
            return
        threading.Thread(target=self.select_gun_with_sign, args=(key_type, key, pressed, toggle, False)).start()

    def select_gun_with_sign(self, key_type, key, pressed=False, toggle=False, auto=False):
        """

        :param pressed:
        :param toggle:
        :param auto:
        :param delay:
        :return:
        """
        if self.select_gun_sign:
            return
        delay = 0
        if key in self.delay_refresh_buttons_map:
            delay = self.delay_refresh_buttons_map[key]
            time.sleep(delay / 1000)
        self.select_gun_sign = True
        start = time.time()
        result = self.select_gun(key_type, key, pressed, toggle, auto)
        self.logger.print_log(f"该次识别延迟：{delay}ms 耗时：{int((time.time() - start) * 1000)}ms")
        self.select_gun_sign = False
        return result

    def get_images_from_bbox(self, bbox_list):
        """
        Get images from specified bounding boxes.

        :param bbox_list: List of bounding boxes [(x1, y1, x2, y2), ...]
        :return: Generator yielding images
        """
        # try:
        #     return list(ImageGrab.grab(bbox=bbox) for bbox in bbox_list)
        # except Exception as e:
        #     self.logger.print_log(f"Error in get_images_from_bbox: {e}")
        return self.screen_taker.get_images_from_bbox(bbox_list)

    def select_gun(self, key_type, key, pressed=False, toggle=False, auto=False):
        """
            使用图片对比，逐一识别枪械，相似度最高设置为current_gun
        :return:
        """
        # cache_key = key_type + ":" + key
        # if cache_key not in self.select_gun_cache:
        #
        if not self.game_windows_status.get_game_windows_status():
            return False

        gun_temp, score_temp = self.image_comparator.compare_with_path(self.image_path,
                                                                       self.get_images_from_bbox([self.bbox]), 0.9, 0.7)
        if gun_temp is None:
            self.logger.print_log("未找到枪械")
            self.current_gun = None
            self.current_scope = None
            self.current_hot_pop = None
        else:
            scope_temp, score_scope_temp = self.image_comparator.compare_with_path(self.scope_path,
                                                                                   self.get_images_from_bbox(
                                                                                       self.scope_bbox), 0.9,
                                                                                   0.4)
            if scope_temp is None:
                self.logger.print_log("未找到配件，默认为1倍")
                scope_temp = '1x'

            if gun_temp in self.has_turbocharger:
                hop_up_temp, score_hop_up_temp = self.image_comparator.compare_with_path(self.hop_up_path,
                                                                                         self.get_images_from_bbox(
                                                                                             self.hop_up_bbox),
                                                                                         0.9, 0.6)
            else:
                hop_up_temp = None
                score_hop_up_temp = 0

            if gun_temp == self.current_gun and scope_temp == self.current_scope and hop_up_temp == self.current_hot_pop:
                self.logger.print_log(
                    "当前枪械搭配已经是: {}-{}-{}".format(self.current_gun, self.current_scope, self.current_hot_pop))
                if auto:
                    return False
            else:
                self.current_scope = scope_temp
                self.current_gun = gun_temp
                self.current_hot_pop = hop_up_temp
                self.logger.print_log(
                    "枪械: {},相似: {}-配件: {},相似: {}-hop_up: {},相似: {}".format(self.current_gun, score_temp,
                                                                                     self.current_scope,
                                                                                     score_scope_temp,
                                                                                     self.current_hot_pop,
                                                                                     score_hop_up_temp))

        for func in self.call_back:
            func(self.current_gun, self.current_scope, self.current_hot_pop)

        return self.current_gun is not None

    def connect(self, func):
        self.call_back.append(func)

    def test(self):
        self.logger.print_log("自动识别初始化中，请稍后……")
        start = time.time()
        self.image_comparator.compare_with_path(self.image_path,
                                                self.get_images_from_bbox([self.bbox]), 0.9, 0.7)
        self.image_comparator.compare_with_path(self.scope_path,
                                                self.get_images_from_bbox(
                                                    self.scope_bbox), 0.9,
                                                0.4)
        self.image_comparator.compare_with_path(self.hop_up_path,
                                                self.get_images_from_bbox(
                                                    self.hop_up_bbox),
                                                0.9, 0.6)
        self.logger.print_log(f"自动识别初始化完毕，耗时[{int((time.time() - start) * 1000)}]")
        self.select_gun_sign = False
