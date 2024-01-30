from core.Config import Config
from core.ReaSnowSelectGun import ReaSnowSelectGun
from core.image_comparator.LocalImageComparator import LocalImageComparator
from log.Logger import Logger
from mouse_mover import MoverFactory
from mouse_mover.MouseMover import MouseMover
from net.socket.NetImageComparator import NetImageComparator
from net.socket.Server import Server

if __name__ == '__main__':
    logger = Logger()
    config = Config(logger)
    if config.read_image_mode == "local":
        image_comparator = LocalImageComparator(logger, config.image_base_path)
    else:
        image_comparator = NetImageComparator(logger, config.image_base_path)
    mouse_mover: MouseMover = MoverFactory.get_mover(logger=logger,
                                                     mouse_model=config.mouse_mover,
                                                     mouse_mover_params=config.mouse_mover_params)
    rea_snow_select_gun = ReaSnowSelectGun(logger=logger, mouse_mover=mouse_mover)
    server = Server(logger=logger, server_address=("127.0.0.1", 12345), image_comparator=image_comparator,
                    select_gun=rea_snow_select_gun)
