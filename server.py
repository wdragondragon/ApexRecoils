import sys

from PyQt5.QtWidgets import QApplication

from core.Config import Config
from core.ReaSnowSelectGun import ReaSnowSelectGun
from core.image_comparator.LocalImageComparator import LocalImageComparator
from log.Logger import Logger
from mouse_mover import MoverFactory
from mouse_mover.MouseMover import MouseMover
from net.socket.NetImageComparator import NetImageComparator
from net.socket.Server import Server
from verification import Check

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Check.check("apex_recoils")
    logger = Logger()
    config = Config(logger=logger, default_ref_config_name="server")
    if config.read_image_mode == "local":
        image_comparator = LocalImageComparator(logger, config.image_base_path)
    else:
        image_comparator = NetImageComparator(logger, config.image_base_path)
    config.mouse_mover = config.server_mouse_mover
    mouse_mover: MouseMover = MoverFactory.get_mover(logger=logger,
                                                     config=config)
    rea_snow_select_gun = ReaSnowSelectGun(logger=logger, mouse_mover=mouse_mover)
    server = Server(logger=logger, server_address=("127.0.0.1", 12345), image_comparator=image_comparator,
                    select_gun=rea_snow_select_gun, mouse_mover=mouse_mover)
    sys.exit(app.exec_())
