import os
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMainWindow

from log.Logger import Logger


class SystemTrayApp(QMainWindow):
    def __init__(self, logger: Logger, icon_path):
        super().__init__()
        self.logger = logger
        self.tray_menu = None
        self.tray_icon = None

        if not QSystemTrayIcon.isSystemTrayAvailable():
            self.logger.print_log("系统托盘不可用")
            return
        path = f"images/{icon_path}.png"

        if not os.path.exists(path):
            bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            path = os.path.join(bundle_dir, f"images/{icon_path}.png")
            if not os.path.exists(path):
                self.logger.print_log("无法找到图标")
        self.icon = QIcon(path)
        if self.icon.isNull():
            self.logger.print_log("无效的图标")
            return

        self.exit_action = QAction("退出", self)
        self.init_icon()

    def init_icon(self):
        self.tray_menu = QMenu(self)
        self.tray_menu.addAction(self.exit_action)
        self.exit_action.triggered.connect(self.exit_app)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

    def exit_app(self):
        self.tray_icon.hide()
        os._exit(0)
