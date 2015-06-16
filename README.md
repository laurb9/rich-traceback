Informative Traceback Logging for Python
===============================================

* Enable informative stack traces if you are already using the standard logging module:
import rich_traceback.enable
import logging

That's it, you can use logging as usual, if an exception happens it will be reported via configured root logger. You can also report exceptions via <yourlog>.exception()

* Save this to test.py and execute:
```
from rich_traceback.formatter import RichTracebackFormatter
import logging

logger = logging.getLogger('root')
console_log = logging.StreamHandler()
console_log.setFormatter(RichTracebackFormatter())
logger.addHandler(console_log)

def foo(x=3):
    if 1.0/x:
        foo(x-1)
try:
    foo()
except:
    logger.exception("error running foo")
```

* Exception traces are generated automatically for uncaught exceptions via an exception hook,
or can be sent explicitly by calling Log.stackTrace() from inside an exception handler.
The format is one frame per line, the order is reversed from the usual tracebacks so the
exception is shown first.

$ python test.py
```
ERROR root test.<module>:15 error running foo
<type 'exceptions.ZeroDivisionError'>: ZeroDivisionError('float division by zero',) ([5] frames following)
[4] test.py, foo(x=0) at line 9: if 1.0/x:
[3] test.py, foo(x=1) at line 10: foo(x-1)
[2] test.py, foo(x=2) at line 10: foo(x-1)
[1] test.py, foo(x=3) at line 10: foo(x-1)
[0] test.py, <module>() at line 13: foo()
```
Syslog traces would get the date and PID as shown below.

* Simple standalone logger with console syslog support.

Log().debug('message')

This will emit the following:
test: __init__:6 got here

And in /var/log/messages (via syslog):
Oct 11 22:17:00 m4600 test[24621]: __init__:6 got here

--
This work is based on the module published with this occasion:
https://mail.python.org/pipermail/python-list/2003-April/202381.html
