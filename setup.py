#!/usr/bin/env python
"""rich traceback setup
 
based on https://packaging.python.org/en/latest/distributing.html
"""

from setuptools import setup, find_packages

setup(
    name='rich-traceback',
    version='1.0.3',
    description='Rich Traceback Logger',
    long_description=('Informative Traceback Logging for Python\n\n'
                      'Informative stack traces showing method parameters\n'
                      'Simple standalone logger with console syslog support.\n'
                      ),
    license='Apache License 2.0',
    author='Laurentiu Badea',
    author_email='laurb9+rich-traceback@gmail.com',
    url='https://github.com/laurb9/rich-traceback',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: No Input/Output (Daemon)',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords='traceback log syslog informative stack traces',

    packages=['rich_traceback'],
    install_requires=[],

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
