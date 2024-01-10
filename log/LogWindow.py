import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QApplication

from log.Logger import Logger


class LogWindow(QMainWindow, Logger):
    """
        日志窗口
    """
    # 类变量用于保存单例实例
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'log_text'):
            self.log_text = None
            self.config = None
            self.init_ui()
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def set_config(self, config):
        self.config = config

    def init_ui(self):
        """
            初始化UI
        """
        self.setWindowTitle("Apex gun")
        self.setGeometry(100, 100, 600, 300)

        # 创建 QTextEdit 组件用于显示日志
        self.log_text = QTextEdit()
        self.log_text.document().setMaximumBlockCount(1000)
        self.log_text.setReadOnly(True)

        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.log_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def print_log(self, log):
        """
            打印日志
        :param log:
        """
        self.log_text.append(log)
        self.log_text.moveCursor(self.log_text.textCursor().End)
        super().print_log(text=log)

    def closeEvent(self, event):
        self.config.save_config()
        QApplication.quit()
        os._exit(0)
