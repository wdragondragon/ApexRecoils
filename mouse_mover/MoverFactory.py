import threading

from core.kmnet_listener.KmBoxNetListener import KmBoxNetListener
from core.kmnet_listener.ToggleKeyListener import ToggleKeyListener
from log import LogFactory
from mouse_mover.FeiMover import FeiMover
from mouse_mover.GHubMover import GHubMover
from mouse_mover.KmBoxMover import KmBoxMover
from mouse_mover.KmBoxNetMover import KmBoxNetMover
from mouse_mover.PanNiMover import PanNiMover
from mouse_mover.Win32ApiMover import Win32ApiMover
from mouse_mover.WuYaMover import WuYaMover
from net.socket.SocketMouseMover import SocketMouseMover


def get_mover(config, mouse_listener=None, mouse_model=None, parent_mover=None, c1_mover=None,
              game_windows_status=None):
    """
        获取键鼠管理器
    """
    if mouse_model is None:
        mouse_model = config.mouse_mover
    mouse_mover_params = config.mouse_mover_params
    mouse_mover_param = mouse_mover_params[mouse_model]
    if mouse_mover_param is None:
        LogFactory.logger().print_log(f"鼠标模式:[{mouse_model}]不可用")
    else:
        LogFactory.logger().print_log(f"初始化鼠标模式：[{mouse_model}]")
    if mouse_model == 'win32api':
        return Win32ApiMover(mouse_mover_param)
    elif mouse_model == "km_box":
        return KmBoxMover(mouse_mover_param)
    elif mouse_model == "wu_ya":
        return WuYaMover(mouse_mover_param)
    elif mouse_model == 'logitech':
        return GHubMover(mouse_mover_param)
    elif mouse_model == "pan_ni":
        return PanNiMover(mouse_mover_param)
    elif mouse_model == "fei_yi_lai" or mouse_model == 'fei_yi_lai_single':
        return FeiMover(mouse_mover_param)
    elif mouse_model == "km_box_net":
        current_mover = KmBoxNetMover(mouse_mover_param)
        if mouse_listener is not None:
            current_mover.listener = KmBoxNetListener(current_mover, mouse_listener)
            threading.Thread(target=current_mover.listener.km_box_net_start).start()
            if parent_mover is None:
                parent_mover = current_mover
            if config.rea_snow_gun_config_name is not None and config.rea_snow_gun_config_name != '':
                current_mover.toggle_key_listener = ToggleKeyListener(km_box_net_listener=current_mover.listener,
                                                                      delayed_activation_key_list=config.delayed_activation_key_list,
                                                                      mouse_mover=parent_mover, c1_mouse_mover=c1_mover,
                                                                      toggle_hold_key=config.toggle_hold_key,
                                                                      game_windows_status=game_windows_status)
        return current_mover
    elif mouse_model == "distributed" or mouse_model == "distributed_c1":
        current_mover = SocketMouseMover(mouse_mover_param=mouse_mover_param,
                                         mode="mouse_mover" if mouse_model == "distributed" else "c1_mouse_mover")
        # server_mover = get_mover(logger=logger, mouse_listener=mouse_listener, config=config,
        #                          mouse_model=config.server_mouse_mover, parent_mover=current_mover, c1_mover=c1_mover,
        #                          game_windows_status=game_windows_status)
        # current_mover.server_mouse_mover = server_mover
        return current_mover
