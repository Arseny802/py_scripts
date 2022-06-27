import logging


class DefaultValues:
    # General setup
    name = 'main'
    level = logging.DEBUG

    # File settings
    directory = 'logs'
    filename = 'script.log'
    filemode = 'a'
    encoding = 'utf-8'
    backup_count = 10

    # Message formatting
    msg_format = '[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s]: %(message)s'
    date_fmt = '%Y-%m-%dT%H:%M:%S'
    utc = True
    delay = True  # do not create file on logger initialization
