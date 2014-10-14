#
# Copyright (C)2014 Laurentiu Badea
#
"""
Test for old logger interface.

TODO: turn into actual unit test.
"""

import rich_traceback.log

log = rich_traceback.log.Log()

def test(name):
    def f(a, b): 
        log.info('executing a/b')
        return a/b
    log.debug('calling f')
    f(5, 0)
    #except: log.exception("While trying to frobnicate")

if __name__ == '__main__':
    test("simple")
