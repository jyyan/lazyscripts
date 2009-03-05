#!/bin/bash
# -*- coding: utf-8 -*-
# Copyright (C) 2008 林哲瑋 Zhe-Wei Lin (billy3321,雨蒼) <bill3321 -AT- gmail.com>
# Last Midified : 5 Mar 2008
# This is a simple bash shell script use to install the packages 
# which need by lazyscripts. This script is use for opensuse with
# i586 architecture.
# Please run as root.


export ARCH_NAME="`uname -a | cut -d " " -f 12`"

echo "正在下載並安裝lazyscripts執行所需的套件...."

zypper install git git-core python-setuptools

zypper install http://lazyscripts.googlecode.com/files/python-nose-0.10.4-3.1.i586.rpm

zypper install http://lazyscripts.googlecode.com/files/python-git-0.1.6-3.1.i586.rpm

echo "執行完畢！即將啟動lazyscripts..."

#END