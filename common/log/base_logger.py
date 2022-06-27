from os import mkdir, path
from logging import Logger, StreamHandler, FileHandler, Formatter
from common.log.default_values import DefaultValues


class BaseLogger(Logger):
    _defaults = DefaultValues()
    __use_console = True

    def __init__(self, name: str = _defaults.name, level: str = _defaults.level, use_console=True):
        super().__init__(name, level)
        self.__use_console = use_console
        if self.__use_console:
            self.addHandler(StreamHandler())

    def reconfigure(
            self,
            filename: str = _defaults.filename,
            filemode: str = _defaults.filemode,
            msg_format: str = _defaults.msg_format,
            date_fmt: str = _defaults.date_fmt):
        for handler in self.handlers:
            handler.setFormatter(Formatter(msg_format, date_fmt))
            if isinstance(handler, FileHandler):
                if handler.baseFilename != filename:
                    self.create_directory(filename)
                    handler.baseFilename = filename
                handler.mode = filemode

    @property
    def get_name(self):
        return self.name

    @property
    def console(self):
        return self.__use_console

    @staticmethod
    def create_directory(filename):
        dir_name = path.dirname(path.relpath(filename))
        if dir_name is not None and dir_name != '' and not path.exists(dir_name):
            mkdir(dir_name)
