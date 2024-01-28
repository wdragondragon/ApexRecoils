import json
import os.path as op

from core.SelectGun import SelectGun
from log.Logger import Logger
from mouse_mover.MouseMover import MouseMover


class ReaSnowSelectGun:
    def __init__(self, logger: Logger, select_gun: SelectGun, mouse_mover: MouseMover):
        self.logger = logger
        self.config_path = ".\\config\\ReaSnowGun.json"
        self.mouse_mover = mouse_mover
        select_gun.connect(self.trigger_button)
        if op.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as global_file:
                self.key_dict = json.load(global_file)

    def trigger_button(self, select_gun, select_scope, hot_pop):

        if select_gun is None or select_scope is None:
            return

        gun_scope_dict = self.key_dict.get(select_gun)
        if gun_scope_dict is None:
            self.logger.print_log(f"枪械[{select_gun}]没有数据，关闭宏")
            self.mouse_mover.click_key(0x35)
            return

        if hot_pop is not None and hot_pop in gun_scope_dict:
            gun_scope_dict = gun_scope_dict[hot_pop]

        first_char = select_scope[0]

        scope_data = gun_scope_dict[first_char]

        if scope_data is not None:
            if "0" in gun_scope_dict:
                scope_data = gun_scope_dict["0"]
                self.logger.print_log(f"枪械[{select_gun}使用通用数据]")
            self.logger.print_log(f"按下键位[{scope_data}]切换数据")
            self.mouse_mover.click_key(int(scope_data, 16))
