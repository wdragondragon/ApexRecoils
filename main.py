import sys
import threading

import pynput
from PyQt5.QtWidgets import QApplication

from core.Config import Config
from core.KeyAndMouseListener import MouseListener, KeyListener
from core.RecoildsCore import RecoilsListener, RecoilsConfig
from core.SelectGun import SelectGun
from log.LogWindow import LogWindow
from mouse_mover import MoverFactory
from mouse_mover.IntentManager import IntentManager
from mouse_mover.MouseMover import MouseMover

if __name__ == '__main__':
    app = QApplication(sys.argv)
    logger = LogWindow()
    config = Config(logger)
    logger.set_config(config)

    apex_mouse_listener = MouseListener(logger=logger)
    apex_key_listener = KeyListener(logger=logger)

    select_gun = SelectGun(logger=logger,
                           bbox=config.select_gun_bbox,
                           image_path=config.image_path,
                           refresh_buttons=config.refresh_buttons)

    mouse_listener = pynput.mouse.Listener(on_click=apex_mouse_listener.on_click)
    keyboard_listener = pynput.keyboard.Listener(on_press=apex_key_listener.on_press,
                                                 on_release=apex_key_listener.on_release)
    mouse_listener_thread = threading.Thread(target=mouse_listener.start)
    keyboard_listener_thread = threading.Thread(target=keyboard_listener.start)

    mouse_listener_thread.start()
    keyboard_listener_thread.start()

    mouse_mover: MouseMover = MoverFactory.get_mover(logger=logger,
                                                     mouse_model=config.mouse_mover,
                                                     mouse_mover_params=config.mouse_mover_params)
    intent_manager = IntentManager(logger=logger, mouse_mover=mouse_mover)
    intent_manager_thread = threading.Thread(target=intent_manager.start)
    intent_manager_thread.start()

    recoils_config = RecoilsConfig(logger=logger)
    recoils_listener = RecoilsListener(logger=logger,
                                       recoils_config=recoils_config,
                                       mouse_listener=apex_mouse_listener,
                                       select_gun=select_gun,
                                       intent_manager=intent_manager)
    recoils_listener_thread = threading.Thread(target=recoils_listener.start)
    recoils_listener_thread.start()

    sys.exit(app.exec_())
