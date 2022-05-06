#
# Copyright (C)2001-2002 InfoStreet, Inc.
#                        Laurentiu Badea lc@infostreet.com
# Copyright (C)2013,2014 Laurentiu Badea
#
"""
Rich traceback logging formatter.

The RichTracebackFormatter class is a drop-in replacement for logging.Formatter.

"""

import sys
import os.path
import inspect
import re
from logging import Formatter

class RichTracebackFormatter(Formatter):
    """
    logging.Formatter subclass for outputting "rich tracebacks"
    """

    DEFAULT_FMT = '%(levelname)s %(name)s %(module)s.%(funcName)s:%(lineno)d %(message)s'
    DEFAULT_DATEFMT = '%Y-%m-%d %H:%M:%S'
    maxParamLength = 512   # parameter values longer than this will be chopped in the middle

    def __init__(self, fmt=None, datefmt=None):
        Formatter.__init__(self, fmt=fmt, datefmt=datefmt)
        self._fmt = fmt or self.DEFAULT_FMT
        self.datefmt = datefmt or self.DEFAULT_DATEFMT


    def formatException(self, ei):
        """
        Generate a rich traceback with inlined method parameters

        :param ei: exception info as returned by sys.exc_info()
        :returns: formatted exception (multiline) string
        """

        (e_type, e_value, traceback_obj) = ei

        try:
            trace = self._format_trace(traceback_obj)
        #except:
        #    return Formatter.formatException(self, ei)
        finally:
            del traceback_obj

        header = "%s: %s ([%d] frames following)" % (repr(e_type), repr(e_value), len(trace))

        trace.reverse()
        return "\n".join([header] + ["[%d] %s, %s" % line for line in trace])


    def _format_value(self, value):
        """
        Format a value into a printable form

        :param value: anything really
        :returns: a string representation of value, usually repr(value)
        """
        # Make prettyargs prettier by removing extra verbiage and addresses
        # pylint: disable=invalid-name
        s = re.sub('<(.+?) at .*?>', lambda m: '<%s>' % m.group(1), repr(value))
        if len(s) > self.maxParamLength:
            s = s[:self.maxParamLength/2] + '......' + s[-self.maxParamLength/2:]
        return '=' + s


    def _format_args(self, frame):
        """
        Extract and format function/method parameters from frame.

        :param frame: Frame object
        :returns: string representing function args, like 'a=5, b=0'
        """
        (args, varargs, varkw, frame_locals) = inspect.getargvalues(frame)
        try:
            prettyargs = inspect.formatargvalues(args, varargs, varkw, frame_locals,
                                                 formatvalue=self._format_value)
        except:  #pylint: disable=bare-except
            prettyargs = '(?)'
        return prettyargs


    def _format_trace(self, traceback_obj=None, levels=2):
        """
        Builds a nicely formatted stack trace as a list of frame data.

        :param tb: optional traceback object
        :param levels: optional caller levels to ignore when autogenerating traceback
                       (if tb is None)
        :returns: a list of [frameNo, moduleName, formattedString] entries
        """

        if traceback_obj:
            frames = inspect.getinnerframes(traceback_obj)
        else:
            frames = inspect.stack()[levels:] # skip this and its caller

        trace = []
        frameNo = 0
        for frame, _, line, function, src, pos in frames:
            code = src[pos].strip() if pos else '(no source)'
            name = self.get_frame_name(frame)
            if function == '?':
                prettyargs = ''
            else:
                prettyargs = self._format_args(frame)

            # here we could separate words in "code" and try to match them in
            # frame.f_locals so we can display the variables involved there.

            trace.append((frameNo, name, "%s%s at line %d: %s" % (function, prettyargs, line, code)))
            frameNo += 1

        return trace


    @classmethod
    def get_frame_name(cls, frame=None):
        """
        Get either the module name or filename if module is __main__.

        :param frame: a Frame object - if None, then the caller's frame is used.
        :returns: module name or filename string
        """

        if not frame:
            frame = sys._getframe().f_back.f_back   # pylint: disable=protected-access

        name = frame.f_globals["__name__"]
        if name == '__main__':
            name = os.path.basename(frame.f_code.co_filename)

        return name
