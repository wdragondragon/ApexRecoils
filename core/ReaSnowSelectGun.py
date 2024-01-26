from core.SelectGun import SelectGun
from log.Logger import Logger


class ReaSnowSelectGun:
    def __init__(self, logger: Logger, select_gun: SelectGun):
        self.logger = logger
        select_gun.connect(self.trigger_button)

    def trigger_button(self, select_gun):
        pass
