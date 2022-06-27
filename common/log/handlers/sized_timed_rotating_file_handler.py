import logging
import os.path
from logging import LogRecord
from pathlib import Path

import time
import logging.handlers as handlers


class SizedTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size, or at certain
    timed intervals
    """

    def __init__(self, filename, max_bytes=0, backup_count=0, encoding=None,
                 delay=0, when='h', interval=1, utc=False):
        os.mkdir(os.path.dirname(os.path.relpath(filename)))
        handlers.TimedRotatingFileHandler.__init__(
            self, filename, when, interval, backup_count, encoding, delay, utc)
        self.maxBytes = max_bytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:  # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:  # are we rolling over?
            msg = "%s\n" % self.format(record)
            # due to non-posix-compliant Windows feature
            self.stream.seek(0, 2)
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        return super().shouldRollover(record)
