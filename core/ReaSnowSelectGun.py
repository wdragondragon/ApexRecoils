import json
import os.path as op

from core.SelectGun import SelectGun
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover


class ReaSnowSelectGun:
    """
        转换器自动识别按键宏触发
    """

    def __init__(self, logger: Logger, mouse_mover: MouseMover):
        self.logger = logger
        self.config_path = ".\\config\\ReaSnowGun.json"
        self.mouse_mover = mouse_mover

        if op.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as global_file:
                self.key_dict = json.load(global_file)

    def trigger_button(self, select_gun, select_scope, hot_pop):
        """

        :param select_gun:
        :param select_scope:
        :param hot_pop:
        :return:
        """
        if select_gun is None or select_scope is None:
            self.mouse_mover.click_key(0x35)
            return

        gun_scope_dict = self.key_dict.get(select_gun)
        if gun_scope_dict is None:
            self.logger.print_log(f"枪械[{select_gun}]没有数据，关闭宏")
            self.mouse_mover.click_key(0x35)
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
        if scope_data is not None:
            self.logger.print_log(f"枪械[{select_gun}]按下键位[{scope_data}]切换数据")
            self.mouse_mover.click_key(int(scope_data, 16))
