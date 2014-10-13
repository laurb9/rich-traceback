#!/usr/bin/env python

from distutils.core import setup

setup(name='python-rich-traceback',
      version='1.0',
      description='Rich Traceback Logger',
      long_description=('Informative Traceback Logging for Python\n\n'
                        'Informative stack traces showing method parameters\n'
                        'Simple standalone logger with console syslog support.\n'
                        ),
      license='GPLv2',
      author='Laurentiu Badea',
      author_email='laurb9+rich-traceback@gmail.com',
      url='https://github.com/laurb9/rich-traceback',
      packages=['rich_traceback'],
     )
