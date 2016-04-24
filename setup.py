#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


packages = [
    'zoomeye',
]

setup (
    name = 'zoomeye',
    version = '1.0',
    py_modules = ['zoomeye'],
    author = 'Magic',
    author_email = '1092070680@qq.com',
    description = 'ZoomEye_API_SDK',
    packages = packages,
)