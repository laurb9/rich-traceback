#!/usr/bin/python
#
# Copyright (C)2001-2002 InfoStreet, Inc.
#                        L.C. (Laurentiu C. Badea) lc@infostreet.com
# GPL-ed on Mar 19, 2003
#
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

## NOTE: sorry I didn't have time to modify this as I promised.

"""logging service using syslog, informative exception stacktraces.

Quick usage:
l = log.Log()

l.debug( 'message' )            # general purpose debugging messages
l.warning( 'message' )          # for warnings
l.error( 'message' )            # errors (exceptions)

NOTE:
Importing this module also activates the new-style exception traces
and exception reporting via syslog.
"""

import sys, traceback, string, os.path, re
import syslog
import inspect # requires python 2.1!

# List of handlers that will be given a chance to display the trace or log
handlers = { }

# These are the syslog logging levels in decreasing order of importance
LOG_EMERG   = syslog.LOG_EMERG;
LOG_ALERT   = syslog.LOG_ALERT;
LOG_CRIT    = syslog.LOG_CRIT;
LOG_ERR     = syslog.LOG_ERR;     # Use this for errors 
LOG_WARNING = syslog.LOG_WARNING; # Use this for warning conditions
LOG_NOTICE  = syslog.LOG_NOTICE;
LOG_INFO    = syslog.LOG_INFO;
LOG_DEBUG   = syslog.LOG_DEBUG;   # Use this for debugging output

# Set to 1 when a global exception occurred that overwrote the context
currentContext = None

class Log:

    def __init__(self, context = None):
        if not context:
            # Try to figure out caller's module (filename)
            callerFrame = sys._getframe().f_back; # won't work for python <2.1
            context = _getName(callerFrame)
        
        self.setContext(context)


    def debug(self, message, priority=LOG_DEBUG, ID=None):
        "Send debugging message"
        self.log(message, priority, ID)

    def warning( self, message, priority=LOG_WARNING, ID=None):
        "Send a warning message"
        self.log(message, priority, ID)

    def error( self, message, priority=LOG_ERR, ID=None):
        "Send an error message"
        self.log(message, priority, ID)

    def log( self, message, priority, ID=None, skiplevels=1 ):
        "Generic log message. ID identifies the location emitting the message"

        if currentContext != self.context:
            self.setContext(self.context, self.options) # reset context
            
        if ID != None:
            whoami = ID
        else:
            frame = sys._getframe().f_back
            while skiplevels:
                frame=frame.f_back
                skiplevels = skiplevels - 1
            
                whoami = "%s:%s " % (frame.f_code.co_name, frame.f_lineno)

        syslog.syslog(priority, whoami + str(message))
    

    def setLevel(self, priority):
        "Filter messages based on the log level - see syslog for priorities"
        syslog.setlogmask(syslog.LOG_UPTO(priority))

    def setLevelMask(self, priorityMask):
        "Filter messages using level mask - see syslog for priorities"
        syslog.setlogmask(priorityMask)

    def setContext(self, context=None, options=0):
        'Initialize syslog lib, set tag name and default options'
        if context:
            self.context = context
            self.options = options
            currentContext = context

        try:
            if sys.stdin.isatty():
                options = options | syslog.LOG_PERROR
        except:
            pass
            
        syslog.openlog(self.context,
                       syslog.LOG_CONS|syslog.LOG_NOWAIT|options,
                       syslog.LOG_LOCAL2) # |syslog.LOG_PID

    def getContext( self ):
        return self.context
    
        
    def stackTrace(self, message=''):
        """log and return stack trace from most recent exception

        call this only after an exception"""
        (type, value, tb) = sys.exc_info()
        return logException( str(type), "%s (%s)" % (message, value), tb )


    def getStackTrace(self):
        "Return the stack trace from most recent exception as a list of lines"
        (type, value, tb) = sys.exc_info()
        return logException( type, str(value), tb, logTrace = 0 )


def logException( type, text, tb, logTrace = 1 ):
    "Catches exceptions that would cause the program to die, logs stack trace."

    "to be used with sys.excepthook"

    try:
        #sys.excepthook(type, text, tb) # output old-style traceback if needed
        trace = _buildStackTrace(tb)
    finally:
        del tb
        
    log = Log(trace[0][1])

    if logTrace:
        log.setContext(options=syslog.LOG_PERROR)

        log.error("Exception %s: '%s' (%d stack frames following, innermost [0])"
                  % (str(type), text, len(trace)), ID='')

    trace.reverse()
    list = []
    for line in trace:
        line = "[%d] %s, %s" % line
        list.append(line)
        if logTrace:
            log.error(line, ID='')
    
    sys.stderr.flush()
    return list


# Set up global exception handler as the above function
sys.excepthook = logException

def _buildStackTrace(tb = None):
    "Builds a nicely formatted stack trace as a list"

    trace  = []
    if tb:
        frameRecords = inspect.getinnerframes(tb)
    else:
        frameRecords = inspect.stack()[2:] # skip this and its caller
        
    i = len(frameRecords)

    def formatValue(value):
        s = repr(value)
        # Make prettyargs prettier by removing extra verbiage and addresses
        s = re.sub('<(.+?) at .*?>', lambda m: '<%s>' % m.group(1), s)
        if len(s) > 512:
            s = s[:256] + '......' + s[-256:]
        return '=' + s
    
    for FR in frameRecords:
        i = i - 1
        frame    = FR[0]
        filename = FR[1]
        line     = FR[2]
        function = FR[3]
        if FR[5] >= 0:
            code = string.strip(FR[4][FR[5]])
        else:
            code = '(source not available)'

        name = _getName(frame)

        # here we could separate words in "code" and try to match them in
        # frame.f_locals so we can display the variables involved there.
            
        if function != '?':
            ( args, varargs, varkw, locals) = inspect.getargvalues(frame)
            try:
                prettyargs = inspect.formatargvalues(args, varargs, varkw, locals, formatvalue=formatValue)
            except:
                prettyargs = "(?)"
        else:
            prettyargs = ''
            
        trace.append( ( i, name,
                        "%s%s at line %d: %s" %
                        (function, prettyargs, line, code) ) )
    
    return trace

def _getName(frame):
    "Return either module name or file's basename if __main__"

    name = frame.f_globals["__name__"]
    if name == "__main__":
        name = os.path.basename(frame.f_code.co_filename)

    return name


def test( y ):
    l = Log()

    print ">>> Testing Debug Message"
    l.debug( "Log Debug Message" )
    print ">>> Testing Warning Message"
    l.warning( "Log Warning Message" )
    print ">>> Testing Error Message"
    l.error( "Log Error Message" )
    print ">>> Testing exception in try-except block"
    try:
        x = 3 / 0
    except Exception:
        l.stackTrace("caught exception test")

    print ">>> Testing uncaught exception in program"
    x = y / 0
    
if __name__ == '__main__':
    test(5)

