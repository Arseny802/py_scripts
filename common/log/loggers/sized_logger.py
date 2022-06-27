import logging
from logging import Logger

from common.log.default_values import DefaultValues


def setup(name: str, level: Logger.level = Logger.level):
    logger = Logger(name)
    logger.setLevel(level)

    logging.basicConfig()


def get(name: str = DefaultValues.name):
    return Logger(name)
