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
import commands
import os
import platform
import locale
import sys

from lazyscripts import config
from lazyscripts import pool
from lazyscripts import template
from lazyscripts import utils
from lazyscripts import pkgmgr as lzspkgmgr

"A directory for caching objects are generated by running lazyscript"
DEFAULT_RUNTIME_ROOT_DIR = '/tmp/lzs_root'

"A file for storaging enviroment variables before sudo"
DEFAULT_STORAGED_ENV_FILE = 'lzs_storagedenv'

#{{{def get_realhome():
def get_realhome():
    "@FIXME ugly way..."
    path = os.path.join(DEFAULT_RUNTIME_ROOT_DIR, DEFAULT_STORAGED_ENV_FILE)
    if not os.path.exists(path):    return os.getenv('HOME')
    lines = open(path, 'r').readlines()
    return ''.join(lines[2][17:]).replace('\n','')
#}}}

#{{{def get_local():
def get_local():
    lang = os.getenv('LANGUAGE')
    if not lang:
        lang = os.getenv('LANG')
    try:
        # zh_TW.UTF-8 or zh_TW:zh.UTF-8
        local = lang[0:5]
    except TypeError:
        local = locale.getlocal(locale.LC_ALL)
        if local:
            local = local[0]
    return local
#}}}

#{{{get_distro_name()
def get_distro_name():
    name = platform.dist()[0]
    if not name:
        if os.path.exists('/etc/arch-release'):
            name = 'arch'
        elif os.path.exists('/usr/bin/pkg') and commands.getoutput('cat /etc/release | grep "OpenSolaris"'):
            name = 'opensolaris'
        else:
            print "Lazyscripts not support your Linux distribution."
            sys.exit()
    elif name == 'redhat':
        if commands.getoutput('cat /etc/redhat-release | grep "Red Hat"'):
            name = 'redhat'
        elif commands.getoutput('cat /etc/redhat-release | grep "CentOS"'):
            name = 'centos'

    return name
#}}}

#{{{get_distro_version(name)
def get_distro_version(name):
    version = platform.dist()[1]
    if not version:
        if name == 'opensolaris':
            version = commands.getoutput('cat /etc/release | grep "OpenSolaris" | cut -d " " -f 27')
    return version
#}}}
    
#{{{get_distro_codename(name)
def get_distro_codename(name):
    codename = platform.dist()[2]
    return codename
#}}}

#{{{get_architecture()
def get_architecture():
    return platform.architecture()[1]
#}}}

#{{{get_laptop_info():
def get_laptop_info():
  """
  get manufacturer, product name.
  """
  if os.getuid() != 0:
    print "ERR: can not get laptop information (root permission requirment)."
    return ()

  cmd = "dmidecode -s %s"
  manuf_name = commands.getoutput(cmd % "system-manufacturer")
  prod_name = commands.getoutput(cmd % "system-product-name")
  return (manuf_name, prod_name)
#}}}


#{{{def get_all_users():
def get_all_users():
        """
        get all users informations in current system.

        @return [$loginanme, $hiddenpwd, $uid, $gid, $real_name, $home_dir, $shell_path]
        """
        #with open('/etc/passwd', 'r') as f:
        f = open('/etc/passwd', 'r') 
        for line in f:
            userinfos = line.strip().split(':')
            uid = int(userinfos[2])
	# only want to get active users.
            if uid < 1000 or uid > 65533:
                continue
            yield userinfos
        f.close()
#}}}

class Register:

    #{{{desc
    """ A python singleton

    the idea is from :http://code.activestate.com/recipes/52558/
    """
    #}}}

    #{{{attrs
    class __impl:
        """ Implementation of the singleton interface """

        workspace = os.path.join(get_realhome(),'.lazyscripts')

        distro = get_distro_name()

        pkgmgr = lzspkgmgr.get_pkgmgr(distro)

    # storage for the instance reference
    __instance = None
    #}}}

    #{{{def __init__(self):
    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if Register.__instance is None:
            # Create and remember instance
            Register.__instance = Register.__impl()

        # Store instance reference as the only member in the handle
        self.__dict__['_Register__instance'] = Register.__instance
    #}}}

    #{{{def __getattr__(self, attr):
    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)
    #}}}

    #{{{def __setattr__(self, attr, value):
    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
    #}}}
pass

#{{{def register_workspace(path=None):
def register_workspace(path=None):
    if path:
        Register().workspace = path

    if not os.path.isdir(Register().workspace):
        template.init_workspace(Register().workspace)
#}}}

#{{{def resource_name(query):
def resource_name(query=None):
    ret = Register().workspace
    if query:
        ret = os.path.join(ret, query)
    return ret
#}}}

#{{{def resource(query):
def resource(query):
    conf = config.Configuration(resource_name('config'))
    if query == 'config':   return conf

    elif query == 'pool':
        poolpath = os.path.join(resource_name('pools'),
                            conf.get_default('pool'))
        return pool.GitScriptsPool(poolpath)
    else:
        raise Exception("QuerryError")
#}}}

#{{{def prepare_runtimeenv():
def prepare_runtimeenv():
    "prepare runtime enviroment which caches objects is generated."
    if not os.path.exists(DEFAULT_RUNTIME_ROOT_DIR):
        return os.mkdir(DEFAULT_RUNTIME_ROOT_DIR, 0755)
#}}}

#{{{def storageenv(path=None):
def storageenv(path=None):
    "Save Bash Shell enviroment variabe."
    mkexport = lambda val: "export REAL_%s=%s" % \
                    (val.upper(),os.getenv(val.upper()))
    distro = platform.dist()[0]
    if not distro:
        if os.path.exists('/etc/arch-release'):
            distro = 'arch'
        elif os.path.exists('/usr/bin/pkg') and commands.getoutput('cat /etc/release | grep "OpenSolaris"'):
            distro = 'opensolaris'

    contents = [
    '#!/bin/bash',
    mkexport('USER'),
    mkexport('HOME'),
    mkexport('LANG'),
    'export DISTRO_ID=%s' % distro
    ]
    if not path:
        path = DEFAULT_RUNTIME_ROOT_DIR
    path = os.path.join(path, 'lzs_storagedenv')
    utils.create_executablefile(path, contents)
    return path
#}}}
