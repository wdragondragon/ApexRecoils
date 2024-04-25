import json
import os.path as op

from core.KeyAndMouseListener import KMCallBack
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover
from tools.Tools import Tools


class AxSelectGun:
    """
        转换器自动识别按键宏触发
    """

    def __init__(self, logger: Logger, mouse_mover: MouseMover, config_name='ReaSnowGun'):
        self.logger = logger
        self.config_path = f".\\config\\{config_name}.json"
        self.mouse_mover = mouse_mover
        if op.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as global_file:
                self.key_dict = json.load(global_file)
        if "close_key" in self.key_dict:
            self.no_macro_key = self.key_dict["close_key"]
        else:
            self.no_macro_key = "3"
        if "open_key" in self.key_dict:
            self.open_key = self.key_dict["open_key"]
        else:
            self.open_key = "0x35"

        self.no_macro_key = Tools.convert_to_decimal(self.no_macro_key)
        self.open_key = Tools.convert_to_decimal(self.open_key)

        # 状态留置
        self.curr_gun_index = 0
        self.gun_cache = [None, None]
        self.refresh_index = [False, False]

        KMCallBack.connect(KMCallBack("k", self.no_macro_key, self.refresh, False))

    def trigger_button(self, select_gun, select_scope, hot_pop, key_type, key):
        """

        :param select_gun:
        :param select_scope:
        :param hot_pop:
        :param key_type:
        :param key:
        :return:
        """
        if select_gun is None or select_scope is None:
            self.logger.print_log(f"未识别到枪械")
            return

        gun_scope_dict = self.key_dict.get(select_gun)
        if gun_scope_dict is None:
            self.logger.print_log(f"枪械[{select_gun}]没有数据")
            return

        if hot_pop is not None and hot_pop in gun_scope_dict:
            gun_scope_dict = gun_scope_dict[hot_pop]

        first_char = select_scope[0]

        if first_char in gun_scope_dict:
            scope_data = gun_scope_dict[first_char]
        else:
            scope_data = None
        if "0" in gun_scope_dict:
            scope_data = gun_scope_dict["0"]
            self.logger.print_log(f"枪械[{select_gun}使用通用数据]")

        # 实现内存中换绑，实际换绑切换是在触发关闭宏时调用refresh执行
        if scope_data is not None and key_type == 'k':
            if key == '1' or key == '2':
                index = int(key)
                self.curr_gun_index = index
            if self.curr_gun_index == 1 or self.curr_gun_index == 2:
                # 该判断有两层逻辑
                # 一、在按下数字时切枪时能动态更换内存中绑定的按键对应的枪械
                # 二、在按下捡枪交互键时，能将curr_gun_index绑定到替换的枪械
                # （会出现落地捡枪不能绑定正确的问题）
                # 所以落地捡枪时最好手动把所有枪切一遍，再使用刷新键触发转换器绑定
                if self.curr_gun_index not in self.gun_cache or self.gun_cache[self.curr_gun_index] != scope_data:
                    self.gun_cache[self.curr_gun_index] = scope_data
                    self.refresh_index[self.curr_gun_index] = True

    def refresh(self):
        if self.refresh_index[0] or self.refresh_index[1]:
            for i, scopen_data in enumerate(self.gun_cache):
                if scopen_data is None or not self.refresh_index[i]:
                    continue
                # todo 按下组合键绑定宏 并开启宏
            # 开启宏
            self.mouse_mover.click_key(self.open_key)
