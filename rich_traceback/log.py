#
# Copyright (C)2014 Laurentiu Badea
#
"""
logging service using syslog, informative exception stacktraces.

Quick usage:
log = log.Log()

log.debug('message')            # general purpose debugging messages
log.warning('message')          # for warnings
log.error('message')            # errors (exceptions)

NOTE:
Importing this module also activates the new-style exception traces.
"""

import sys
import logging
import logging.handlers
from .formatter import RichTracebackFormatter

LOG_ERR = logging.ERROR
LOG_WARNING = logging.WARNING
LOG_INFO = logging.INFO
LOG_DEBUG = logging.DEBUG

class Log(object):
    """
    Backwards-compatible Log class, for use as example.
    """

    LOG_FMT = '%(levelname)s %(name)s %(message)s'

    def __init__(self):
        name = RichTracebackFormatter.get_frame_name()
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # create console handler
        con_log = logging.StreamHandler(sys.stderr)
        con_log.setLevel(logging.DEBUG)

        # create syslog handler
        sys_log = logging.handlers.SysLogHandler('/dev/log')
        sys_log.setLevel(logging.WARN)

        # create formatter(s) and add to the handlers
        con_log.setFormatter(RichTracebackFormatter('%(asctime)s ' + self.LOG_FMT))
        sys_log.setFormatter(RichTracebackFormatter(self.LOG_FMT))

        # add the handlers to the logger
        self.logger.addHandler(con_log)
        self.logger.addHandler(sys_log)


    def debug(self, message, *args):
        """Send a debugging message"""
        self.logger.log(LOG_DEBUG, message, *args)


    def info(self, message, *args):
        """Send an info message"""
        self.logger.log(LOG_INFO, message, *args)


    def warning(self, message, *args):
        """Send a warning message"""
        self.logger.log(LOG_WARNING, message, *args)


    def error(self, message, *args):
        """Send an error message"""
        self.logger.log(LOG_ERR, message, *args)


    def exception(self, message, exc_info=None, *args):
        """Send a stack trace after exception"""
        self.logger.log(LOG_ERR, message, exc_info=(exc_info or sys.exc_info()), *args)

    stackTrace = exception   # old name


# Override logging.Formatter class because we don't have a way to set a module default
# (logging._defaultFormatter is not used everywhere)
if not issubclass(logging.Formatter, RichTracebackFormatter):
    logging.Formatter = RichTracebackFormatter


# Set up global exception handler as the above function
sys.excepthook = lambda *ei: Log().exception("Uncaught Exception", exc_info=ei)
