import os.path as op
import json
import time

import requests
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
        self.specs_data = None
        self.load()

    def load(self):
        """
            加载压枪数据
        """
        config_file_path = 'config\\specs.json'
        if op.exists(config_file_path):
            with open(config_file_path, encoding='utf8') as file:
                self.specs_data = json.load(file)
                self.logger.print_log("加载配置文件: {}".format(config_file_path))
        else:
            config_json_str = RecoilsConfig.read_file_from_url("http://1.15.138.227:9000/apex/specs.json")
            self.specs_data = json.loads(config_json_str)
            self.logger.print_log("加载配置文件成功")

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

    @staticmethod
    def read_file_from_url(url):
        """

        :param url:
        :return:
        """
        try:
            # 发送GET请求获取文件内容
            # headers = random.choice(headers_list)
            response = requests.get(url)
            response.encoding = 'utf-8'
            # 检查请求是否成功
            if response.status_code == 200:
                # 根据换行符切割文件内容并返回列表
                text = response.text
                return text
            else:
                print(f"Failed to read file from URL. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
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
                 intent_manager: IntentManager, game_windows_status):
        self.logger = logger
        self.recoils_config = recoils_config
        self.mouse_listener = mouse_listener
        self.select_gun = select_gun
        self.intent_manager = intent_manager
        self.game_windows_status = game_windows_status

    def start(self):
        """
            开始监听
        """
        start_time = None
        num = 0
        sleep_time = 0.001
        while True:
            if not self.game_windows_status.get_game_windows_status():
                time.sleep(1)
                continue
            current_gun = self.select_gun.current_gun
            left_press = self.mouse_listener.is_press(Button.left)
            right_press = self.mouse_listener.is_press(Button.right)
            if current_gun is not None and left_press:
                current_hot_pop = self.select_gun.current_hot_pop
                spec = self.recoils_config.get_config(current_gun)
                if spec is not None:
                    spec = spec['recoils']
                    if current_hot_pop is not None and current_hot_pop in spec:
                        spec = spec[current_hot_pop]
                    if start_time is None:
                        start_time = time.time()
                        self.logger.print_log("开始压枪")
                    if right_press:
                        spec = spec['aim']
                    else:
                        spec = spec['un_aim']
                    time_points = spec['time_points']
                    if len(time_points) == 0:
                        time.sleep(0.01)
                        continue
                    sleep_time = 0.001
                    point = (time.time() - start_time) * 1000
                    index = len(time_points) - 1 if point > time_points[-1] else next(
                        (i - 1 for i, time_point in enumerate(time_points) if time_point > point),
                        -1)
                    if index is not None and index >= 0 and num <= index:
                        # 获取对应下标的x和y
                        x_values = spec['x']
                        y_values = spec['y']
                        if len(x_values) >= num + 1:
                            x_value = x_values[num]
                            y_value = y_values[num]
                            self.logger.print_log(
                                f'执行时间：[{time_points[num]}]<[{point}],正在压第{str(num + 1)}步，剩余{str(len(time_points) - (num + 1))}步，鼠标移动轨迹为({x_value},{y_value})')
                            # self.intent_manager.set_intention(x_value, y_value)
                            self.intent_manager.mouse_mover.move_rp(x_value, y_value)
                        else:
                            self.logger.print_log(
                                f'缺失第[{num + 1}个轨迹，时间为{time_points[num]}])')
                        num += 1
                else:
                    self.logger.print_log(f"未找到[{current_gun}的压枪数据]")
            else:
                start_time = None
                num = 0
                sleep_time = 0.01
            if sleep_time != 0:
                time.sleep(sleep_time)
