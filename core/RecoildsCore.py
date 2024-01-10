import os.path as op
import json
import time

from pynput.mouse import Button

from core.KeyAndMouseListener import MouseListener
from core.SelectGun import SelectGun
from log.Logger import Logger
from mouse_mover.IntentManager import IntentManager


class RecoilsConfig:
    """
        枪械配置后座力配置
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        config_file_path = 'config\\specs.json'
        if op.exists(config_file_path):
            with open(config_file_path) as file:
                self.specs_data = json.load(file)
                self.logger.print_log("加载配置文件: {}".format(config_file_path))
        else:
            self.logger.print_log("配置文件不存在: {}".format(config_file_path))

    def get_config(self, name):
        """
            根据枪协名称获取后座力数据
        :param name:
        :return:
        """
        for spec in self.specs_data:
            if spec['name'] == name:
                return spec
        return None


class RecoilsListener:
    """
        压枪监听，监听到开火，将识别到的枪械名称配置读取，然后推送到移动意图管理器中
    """

    def __init__(self,
                 logger: Logger,
                 recoils_config: RecoilsConfig,
                 mouse_listener: MouseListener,
                 select_gun: SelectGun,
                 intent_manager: IntentManager):
        self.logger = logger
        self.recoils_config = recoils_config
        self.mouse_listener = mouse_listener
        self.select_gun = select_gun
        self.intent_manager = intent_manager

    def start(self):
        """
            开始监听
        """
        start_time = None
        i = 0
        sleep_time = 0.001
        while True:
            current_gun = self.select_gun.current_gun
            if current_gun is not None and self.mouse_listener.is_press(Button.left) and self.mouse_listener.is_press(
                    Button.right):
                spec = self.recoils_config.get_config(current_gun)
                if spec is not None:
                    if start_time is None:
                        self.logger.print_log("开始压枪")
                        start_time = time.time()
                    time_points = spec['time_points']
                    point = (time.time() - start_time) * 1000
                    index = next(
                        (i for i, time_point in enumerate(time_points) if
                         time_point >= point),
                        None)
                    if index is not None and i < index:
                        # 获取对应下标的x和y
                        x_values = spec['x']
                        y_values = spec['y']
                        if len(x_values) >= index + 1:
                            x_value = x_values[index]
                            y_value = y_values[index]
                            self.logger.print_log(
                                f'执行时间：[{point}]<[{time_points[index]}],正在压第{str(index)}枪，鼠标移动轨迹为({x_value},{y_value})')
                            self.intent_manager.set_intention(x_value, y_value)
                        else:
                            self.logger.print_log(
                                f'缺失轨迹：第[{point}，时间为{time_points[index]}])')
                        i = index
                else:
                    self.logger.print_log(f"未找到[{current_gun}的压枪数据]")
            else:
                start_time = None
                i = 0
            time.sleep(sleep_time)
