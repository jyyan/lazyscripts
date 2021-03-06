#!/usr/bin/env python
# -*- encoding=utf8 -*-
#
# Copyright © 2010 Hsin Yi Chen
#
# Lazyscripts is a free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This software is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this software; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
import glob
import os

try:
    from setuptools import find_packages
except ImportError:
    print "please install python-setuptools first"

from distutils.core import setup
from distutils.command.install import install

setup(
    name = 'Lazyscripts',
    version = '0.2.3.9',
    description = 'The scripts manager in Linux.',
    long_description = """
Lazyscripts is just a scripts distrubtion tool and quick-installer in linux, which aims to provide a easy way to setup your working enviroment for people who need to install a new distrubution such as Debian,Ubuntu, or who want to have much better experiences in linux.

The original idea is from LazyBuntu, made by PCman in Taiwan. we usually need the script to customize to get somthing better, but theses customization may very hard to end users who new to linux, even the experienced end users. so that is why the lazyscript project starts.
""",
    author = 'Hsin Yi Chen 陳信屹 (hychen)',
    author_email = 'ossug.hychen@gmail.com',
    license = 'GPLv2',
    url = 'http://www.lazyscripts.org',
    packages = find_packages(exclude=['tests']),
    scripts = ['scripts/lzs','scripts/glzs'],
    test_suite = 'tests.suite',
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['config']
    },
    zip_safe=False,
    cmdclass = {'install': install},
    data_files = []
)
