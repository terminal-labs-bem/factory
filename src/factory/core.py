import os
import sys
import platform
from os import listdir
from os.path import isfile, join
import importlib
import importlib.util
import os
import shutil
import urllib
import subprocess
from pathlib import Path, PurePath
from urllib.request import urlopen
from os.path import isdir, dirname, realpath, abspath, join, exists
from zipfile import ZipFile
from configparser import ConfigParser
import pkg_resources

import psutil

from lowkit.initialization.workingset import setup_workingset

def isWritable(path: str) -> bool:
    try:
        filename  = os.path.join(path, 'write_test')
        f = open(filename,"w")
        f.close()
        os.remove(filename)
        return True
    except:
        return False

def in_venv():
    return sys.prefix != sys.base_prefix

def get_fs_type(mypath):
    root_type = ""
    for part in psutil.disk_partitions():
        if part.mountpoint == '/':
            root_type = part.fstype
            continue

        if mypath.startswith(part.mountpoint):
            return part.fstype

    return root_type

def initapp():
    setup_workingset()
    # print(isWritable(os.getcwd()))
    # print(get_fs_type("/"))
    # #for name, value in os.environ.items():
    # #    print("{0}: {1}".format(name, value))
    # corepath = Path(__file__)
    # print(in_venv())
    # invocationdir = os.getcwd()
    # print(invocationdir)
    # print(os.environ['VIRTUAL_ENV'])
    # print(psutil.Process().memory_info().rss / (1024 * 1024))
    # print(psutil.virtual_memory().percent)
    # print(platform.python_version())
    # print(sys.version)
    # print(sys.platform, platform.platform())
    # print(platform.freedesktop_os_release())
    # print(corepath)
    # installed_packages = pkg_resources.working_set
    # installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    # print(len(installed_packages_list))
    

