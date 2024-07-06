import sys
import threading

import pynput
from PyQt5.QtWidgets import QApplication

from auth.check_run import open_check
from core.Config import Config
from core.GameWindowsStatus import GameWindowsStatus
from core.KeyAndMouseListener import MouseListener, KeyListener
from core.ReaSnowSelectGun import ReaSnowSelectGun
from core.RecoildsCore import RecoilsListener, RecoilsConfig
from core.SelectGun import SelectGun
from core.image_comparator import ImageComparatorFactory
from core.image_comparator.DynamicSizeImageComparator import DynamicSizeImageComparator
from core.joy_listener.JoyListener import JoyListener
from core.joy_listener.JoyToKey import JoyToKey
from core.joy_listener.RockerMonitor import RockerMonitor
from core.joy_listener.S1SwitchMonitor import S1SwitchMonitor
from core.screentaker import ScreenTakerFactory
from log import LogFactory
from mouse_mover import MoverFactory
from mouse_mover.IntentManager import IntentManager
from mouse_mover.MouseMover import MouseMover
from windows.SystemTrayApp import SystemTrayApp


@open_check("apex_recoils")
def main():
    """
        main
    """
    app = QApplication(sys.argv)
    LogFactory.init_logger("client")
    config = Config(default_ref_config_name="client")

    apex_mouse_listener = MouseListener()
    apex_key_listener = KeyListener()

    game_windows_status = GameWindowsStatus()

    image_comparator = ImageComparatorFactory.get_image_comparator(comparator_mode=config.comparator_mode,
                                                                   config=config)

    screen_taker = ScreenTakerFactory.get_screen_taker(config.screen_taker, config.distributed_param)

    select_gun = SelectGun(bbox=config.select_gun_bbox,
                           image_path=config.image_path,
                           scope_bbox=config.select_scope_bbox,
                           scope_path=config.scope_path,
                           refresh_buttons=config.refresh_buttons,
                           has_turbocharger=config.has_turbocharger,
                           hop_up_bbox=config.select_hop_up_bbox,
                           hop_up_path=config.hop_up_path,
                           image_comparator=image_comparator,
                           screen_taker=screen_taker, game_windows_status=game_windows_status,
                           delay_refresh_buttons=config.delay_refresh_buttons)

    mouse_listener = pynput.mouse.Listener(on_click=apex_mouse_listener.on_click)
    keyboard_listener = pynput.keyboard.Listener(on_press=apex_key_listener.on_press,
                                                 on_release=apex_key_listener.on_release)
    mouse_listener_thread = threading.Thread(target=mouse_listener.start)
    keyboard_listener_thread = threading.Thread(target=keyboard_listener.start)

    mouse_listener_thread.start()
    keyboard_listener_thread.start()

    mouse_mover: MouseMover = MoverFactory.get_mover(mouse_listener=apex_mouse_listener,
                                                     game_windows_status=game_windows_status,
                                                     config=config)
    intent_manager = IntentManager(mouse_mover=mouse_mover)
    intent_manager_thread = threading.Thread(target=intent_manager.start)
    intent_manager_thread.start()

    # 如果需要对接s1
    # 1. 识别触发s1按键，使用rea_snow_mouse_mover
    # 2. s1的切换逻辑层的按键保持，使用rea_snow_mouse_mover
    # 3. jtk，根据key_trigger_mode来选择 mouse_mover的配置还是固定的distributed_c1
    if config.rea_snow_gun_config_name != '':
        # 判断c1透传
        if config.rea_snow_mouse_mover == config.mouse_mover:
            rea_snow_mouse_mover = mouse_mover
        else:
            rea_snow_mouse_mover: MouseMover = MoverFactory.get_mover(mouse_listener=apex_mouse_listener,
                                                                      config=config,
                                                                      mouse_model=config.rea_snow_mouse_mover,
                                                                      c1_mover=mouse_mover,
                                                                      game_windows_status=game_windows_status)
        rea_snow_select_gun = ReaSnowSelectGun(mouse_mover=rea_snow_mouse_mover,
                                               config_name=config.rea_snow_gun_config_name)
        select_gun.connect(rea_snow_select_gun.trigger_button)

        if config.key_trigger_mode == 'local':
            c1_mover: MouseMover = mouse_mover
        else:
            c1_mover: MouseMover = MoverFactory.get_mover(config=config, mouse_model="distributed_c1")

        joy_listener = JoyListener()
        dynamic_size_image_comparator = DynamicSizeImageComparator(base_path=config.image_base_path,
                                                                   screen_taker=screen_taker)
        s1_switch_monitor = S1SwitchMonitor(joy_listener=joy_listener,
                                            licking_state_path=config.licking_state_path,
                                            licking_state_bbox=config.licking_state_bbox,
                                            mouser_mover=rea_snow_mouse_mover,
                                            dynamic_size_image_comparator=dynamic_size_image_comparator,
                                            s1_switch_hold_map=config.s1_switch_hold_map)
        # jtk启动
        jtk = JoyToKey(joy_to_key_map=config.joy_to_key_map, c1_mouse_mover=c1_mover,
                       game_windows_status=game_windows_status)
        joy_listener.connect_axis(jtk.axis_to_key)
        rocker_monitor = RockerMonitor(joy_listener=joy_listener, select_gun=select_gun)
        joy_listener.start(None)
    else:
        # 压枪
        recoils_config = RecoilsConfig()
        recoils_listener = RecoilsListener(recoils_config=recoils_config,
                                           mouse_listener=apex_mouse_listener,
                                           select_gun=select_gun,
                                           intent_manager=intent_manager,
                                           game_windows_status=game_windows_status)
        recoils_listener_thread = threading.Thread(target=recoils_listener.start)
        recoils_listener_thread.start()

    system_tray_app = SystemTrayApp("client")
    # 自动识别启动
    threading.Thread(target=select_gun.test).start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
