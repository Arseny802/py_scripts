import logging

from common.log.default_values import DefaultValues
from common.log.loggers.daily_logger import DailyLogger

logging.Logger = DailyLogger("common", 'common.log')

all_loggers = dict()


def create_logger(name: str = DefaultValues.name, module: str = None):
    all_loggers[name] = DailyLogger(
        name,
        DefaultValues.filename if module is None else module + '.log')
    return all_loggers[name]


def get_logger(name: str = DefaultValues.name, module: str = None):
    result = all_loggers.get(name)
    return result if result is not None else create_logger(name, module)
