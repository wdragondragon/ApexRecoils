import sys
import threading

import pynput
from PyQt5.QtWidgets import QApplication

from core.Config import Config
from core.GameWindowsStatus import GameWindowsStatus
from core.KeyAndMouseListener import MouseListener, KeyListener
from core.ReaSnowSelectGun import ReaSnowSelectGun
from core.RecoildsCore import RecoilsListener, RecoilsConfig
from core.SelectGun import SelectGun
from core.image_comparator import ImageComparatorFactory
from core.screentaker import ScreenTakerFactory
from log.Logger import Logger
from mouse_mover import MoverFactory
from mouse_mover.IntentManager import IntentManager
from mouse_mover.MouseMover import MouseMover
from verification import Check
from windows.SystemTrayApp import SystemTrayApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Check.check("apex_recoils")
    logger = Logger()
    config = Config(logger=logger, default_ref_config_name="client")
    # logger.set_config(config)

    apex_mouse_listener = MouseListener(logger=logger)
    apex_key_listener = KeyListener(logger=logger)

    game_windows_status = GameWindowsStatus(logger=logger)

    image_comparator = ImageComparatorFactory.get_image_comparator(logger=logger,
                                                                   comparator_mode=config.comparator_mode,
                                                                   config=config)

    screen_taker = ScreenTakerFactory.get_screen_taker(logger, config.screen_taker, config.distributed_param)

    select_gun = SelectGun(logger=logger,
                           bbox=config.select_gun_bbox,
                           image_path=config.image_path,
                           scope_bbox=config.select_scope_bbox,
                           scope_path=config.scope_path,
                           refresh_buttons=config.refresh_buttons,
                           has_turbocharger=config.has_turbocharger,
                           hop_up_bbox=config.select_hop_up_bbox,
                           hop_up_path=config.hop_up_path,
                           image_comparator=image_comparator,
                           screen_taker=screen_taker, game_windows_status=game_windows_status)

    mouse_listener = pynput.mouse.Listener(on_click=apex_mouse_listener.on_click)
    keyboard_listener = pynput.keyboard.Listener(on_press=apex_key_listener.on_press,
                                                 on_release=apex_key_listener.on_release)
    mouse_listener_thread = threading.Thread(target=mouse_listener.start)
    keyboard_listener_thread = threading.Thread(target=keyboard_listener.start)

    mouse_listener_thread.start()
    keyboard_listener_thread.start()

    mouse_mover: MouseMover = MoverFactory.get_mover(logger=logger,
                                                     mouse_listener=apex_mouse_listener,
                                                     config=config)
    intent_manager = IntentManager(logger=logger, mouse_mover=mouse_mover)
    intent_manager_thread = threading.Thread(target=intent_manager.start)
    intent_manager_thread.start()

    # 压枪
    recoils_config = RecoilsConfig(logger=logger)
    recoils_listener = RecoilsListener(logger=logger,
                                       recoils_config=recoils_config,
                                       mouse_listener=apex_mouse_listener,
                                       select_gun=select_gun,
                                       intent_manager=intent_manager)
    recoils_listener_thread = threading.Thread(target=recoils_listener.start)
    recoils_listener_thread.start()

    # logger.set_recoils_config(recoils_config)

    # if config.shake_gun_toggle:
    #     shake_gun: ShakeGun = ShakeGun(logger=logger, config=config, mouse_listener=apex_mouse_listener,
    #                                    mouse_mover=mouse_mover,
    #                                    select_gun=select_gun)

    # 判断c1透传
    if config.rea_snow_mouse_mover == config.mouse_mover:
        rea_snow_select_gun = ReaSnowSelectGun(logger=logger, mouse_mover=mouse_mover,
                                               config_name=config.rea_snow_gun_config_name)
    else:
        rea_snow_mouse_mover: MouseMover = MoverFactory.get_mover(logger=logger,
                                                                  mouse_listener=apex_mouse_listener,
                                                                  config=config,
                                                                  mouse_model=config.rea_snow_mouse_mover,
                                                                  c1_mover=mouse_mover)
        rea_snow_select_gun = ReaSnowSelectGun(logger=logger, mouse_mover=rea_snow_mouse_mover,
                                               config_name=config.rea_snow_gun_config_name)
    select_gun.connect(rea_snow_select_gun.trigger_button)

    # jtk启动，挪到server运行
    # jtk = JoyToKey(logger=logger, joy_to_key_map=config.joy_to_key_map, c1_mouse_mover=mouse_mover)
    # joy_listener = JoyListener(logger=logger)
    # joy_listener.connect_axis(jtk.axis_to_key)
    # joy_listener.start(None)
    system_tray_app = SystemTrayApp(logger, "client")
    # 自动识别启动
    threading.Thread(target=select_gun.test).start()
    sys.exit(app.exec_())
