#
# Copyright (C)2014 Laurentiu Badea
#
"""
Alter global logging module by replacing the Formatter class with RichTracebackFormatter
Install exception hook that prints out rich traceback.
"""
import sys
from .formatter import RichTracebackFormatter
import logging

if not RichTracebackFormatter in logging.Formatter.mro():   # pylint: disable=no-member
    logging.Formatter = RichTracebackFormatter

# Set up global exception handler as the above function
sys.excepthook = lambda *ei: logging.error("Uncaught Exception", exc_info=ei)
