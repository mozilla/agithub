#!/usr/bin/env python
from distutils.core import setup

setup(name='agithub',
      version='1.3',
      author='Jonathan Paugh',
      url='https://github.com/jaredhobbs/agithub',
      description="The agnostic Github API. It doesn't know, "
                  "and you don't care.",
      py_modules=['agithub'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      keywords=['github', 'api'])
