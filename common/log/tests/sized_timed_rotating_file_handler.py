import logging
import unittest
import time

from common.log.handlers.sized_timed_rotating_file_handler import SizedTimedRotatingFileHandler


class MyTestCase(unittest.TestCase):
    logger_name = 'SizedTimedRotatingFileHandlerTest'
    log_filename = 'logs/test_log_sized_rotate.log'
    log_level = logging.DEBUG
    logger = None

    def setUp(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(self.log_level)
        handler = SizedTimedRotatingFileHandler(
            self.log_filename,
            max_bytes=1024,
            backup_count=5,
            when='s',
            interval=10,
            # encoding='bz2',  # uncomment for bz2 compression
        )
        self.logger.addHandler(handler)

    def test_something(self):
        for i in range(10000):
            time.sleep(0.1)
            self.logger.debug('i=%d' % i)


if __name__ == '__main__':
    unittest.main()
