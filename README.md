Informative Traceback Logging for Python
===============================================


This work is based on the module published with this occasion:
https://mail.python.org/pipermail/python-list/2003-April/202381.html

* Simple standalone logger with console syslog support.

Log().debug('message')

This will emit the following:
test: __init__:6 got here

And in /var/log/messages (via syslog):
Oct 11 22:17:00 m4600 test[24621]: __init__:6 got here

* Exception traces are generated automatically for uncaught exceptions via an exception hook,
or can be sent explicitly by calling Log.stackTrace() from inside an exception handler.
The format is one frame per line, the order is reversed from the usual tracebacks so the
exception is shown first.

```
log.py: Exception <type 'exceptions.ZeroDivisionError'>: 'integer division or modulo by zero' (2 stack frames following, innermost [0])
log.py: [0] log.py, test(y=5) at line 252: x = y / 0
log.py: [1] log.py, <module>() at line 255: test(5)
```

Syslog traces would get the date and PID just like the above.
