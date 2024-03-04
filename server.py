import sys
import threading

from PyQt5.QtWidgets import QApplication

from core.Config import Config
from core.GameWindowsStatus import GameWindowsStatus
from core.ReaSnowSelectGun import ReaSnowSelectGun
from core.image_comparator.LocalImageComparator import LocalImageComparator
from core.joy_listener.JoyListener import JoyListener
from core.joy_listener.JoyToKey import JoyToKey
from core.screentaker.LocalScreenTaker import LocalScreenTaker
from log.Logger import Logger
from mouse_mover import MoverFactory
from mouse_mover.MouseMover import MouseMover
from net.socket.NetImageComparator import NetImageComparator
from net.socket.Server import Server
from verification import Check
from windows.SystemTrayApp import SystemTrayApp

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Tools.hide_process()

    Check.check("apex_recoils")
    logger = Logger()
    config = Config(logger=logger, default_ref_config_name="server")
    game_windows_status = GameWindowsStatus(logger=logger)

    if config.read_image_mode == "local":
        image_comparator = LocalImageComparator(logger, config.image_base_path)
    else:
        image_comparator = NetImageComparator(logger, config.image_base_path)

    mouse_mover: MouseMover = MoverFactory.get_mover(logger=logger,
                                                     config=config,
                                                     mouse_model=config.server_mouse_mover,
                                                     game_windows_status=game_windows_status)
    rea_snow_select_gun = ReaSnowSelectGun(logger=logger, mouse_mover=mouse_mover,
                                           config_name=config.rea_snow_gun_config_name)

    c1_mouse_mover: MouseMover = MoverFactory.get_mover(logger=logger,
                                                        config=config,
                                                        mouse_model=config.mouse_mover,
                                                        game_windows_status=game_windows_status)
    # jtk启动
    jtk = JoyToKey(logger=logger, joy_to_key_map=config.joy_to_key_map, c1_mouse_mover=c1_mouse_mover,
                   game_windows_status=game_windows_status)
    joy_listener = JoyListener(logger=logger)
    joy_listener.connect_axis(jtk.axis_to_key)
    joy_listener.start(None)
    system_tray_app = SystemTrayApp(logger, "server")
    server = Server(logger=logger, server_address=(config.distributed_param["ip"], config.distributed_param["port"]),
                    image_comparator=image_comparator,
                    select_gun=rea_snow_select_gun, mouse_mover=mouse_mover, screen_taker=LocalScreenTaker(logger))
    threading.Thread(target=server.wait_client).start()
    sys.exit(app.exec_())
