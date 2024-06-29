import sys
import threading

from PyQt5.QtWidgets import QApplication

from core.Config import Config
from core.GameWindowsStatus import GameWindowsStatus
from core.ReaSnowSelectGun import ReaSnowSelectGun
from core.image_comparator.LocalImageComparator import LocalImageComparator
from core.screentaker.LocalScreenTaker import LocalScreenTaker
from log import LogFactory
from mouse_mover import MoverFactory
from mouse_mover.MouseMover import MouseMover
from net.socket.NetImageComparator import NetImageComparator
from net.socket.Server import Server
from verification import Check
from windows.SystemTrayApp import SystemTrayApp

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Tools.hide_process()
    LogFactory.init_logger("server")
    Check.check("apex_recoils")
    config = Config(default_ref_config_name="server")
    game_windows_status = GameWindowsStatus()

    if config.read_image_mode == "local":
        image_comparator = LocalImageComparator(config.image_base_path)
    else:
        image_comparator = NetImageComparator(config.image_base_path)

    mouse_mover: MouseMover = MoverFactory.get_mover(config=config,
                                                     mouse_model=config.server_mouse_mover,
                                                     game_windows_status=game_windows_status)
    rea_snow_select_gun = None
    if config.rea_snow_gun_config_name != '':
        rea_snow_select_gun = ReaSnowSelectGun(mouse_mover=mouse_mover,
                                               config_name=config.rea_snow_gun_config_name)

    c1_mouse_mover: MouseMover = MoverFactory.get_mover(config=config,
                                                        mouse_model=config.mouse_mover,
                                                        game_windows_status=game_windows_status)

    system_tray_app = SystemTrayApp("server")
    server = Server(server_address=(config.distributed_param["ip"], config.distributed_param["port"]),
                    image_comparator=image_comparator,
                    select_gun=rea_snow_select_gun,
                    mouse_mover=mouse_mover,
                    c1_mouse_mover=c1_mouse_mover,
                    screen_taker=LocalScreenTaker())
    threading.Thread(target=server.wait_client).start()
    sys.exit(app.exec_())
