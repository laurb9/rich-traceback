#
# Copyright (C)2014 Laurentiu Badea
#
"""
Test RichTracebackFormatter class.

"""

import unittest
import logging
import rich_traceback.formatter
import StringIO

class LogTest(unittest.TestCase):

    def testLogException(self):
        output = StringIO.StringIO()
        self.logger = logging.getLogger('root')
        self.logger.setLevel(logging.DEBUG)
        con_log = logging.StreamHandler(output)
        con_log.setLevel(logging.DEBUG)
        con_log.setFormatter(rich_traceback.formatter.RichTracebackFormatter())
        self.logger.addHandler(con_log)
        
        def f(a, b):
            self.logger.info('executing a/b')
            return a/b
        self.logger.debug('calling f')
        try:
            f(5, 0)
        except: 
            self.logger.exception("While trying to frobnicate")
        
        self.assertEqual(output.getvalue(), """\
DEBUG root formatter_test.testLogException:28 calling f
INFO root formatter_test.f:26 executing a/b
ERROR root formatter_test.testLogException:32 While trying to frobnicate
<type 'exceptions.ZeroDivisionError'>: ZeroDivisionError('integer division or modulo by zero',) (2 frames following)
  formatter_test, f(a=5, b=0) at line 27: return a/b
  formatter_test, testLogException(self=<formatter_test.LogTest testMethod=testLogException>) at line 30: f(5, 0)
""")
