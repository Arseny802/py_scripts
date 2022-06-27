from logging import Logger
from logging.handlers import TimedRotatingFileHandler

from common.log.base_logger import BaseLogger
from common.log.default_values import DefaultValues


def get(name: str = DefaultValues.name):
    return Logger(name)


class DailyLogger(BaseLogger):
    __when = 'd'

    def __init__(self, logger_name: str, filename: str, use_console=True, backup_count: int = 30):
        super().__init__(logger_name, use_console=use_console)
        self._defaults.backup_count = backup_count
        filename = self._defaults.directory + '//' + filename
        self.create_directory(filename)
        self.__handler = TimedRotatingFileHandler(
            filename=filename,
            when=self.__when,
            interval=1,  # How many days should pass
            backupCount=backup_count,
            utc=self._defaults.utc,
            delay=self._defaults.delay)
        self.addHandler(self.__handler)
        self.reconfigure(filename=filename)

    def set_interval(self, interval: int):
        self.__handler.interval = interval

    def get_interval(self):
        return self.__handler.interval
