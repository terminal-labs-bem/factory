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
        filename = os.path.join(path, "write_test")
        f = open(filename, "w")
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
        if part.mountpoint == "/":
            root_type = part.fstype
            continue

        if mypath.startswith(part.mountpoint):
            return part.fstype

    return root_type

class AppContext:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AppContext, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        installed_packages = pkg_resources.working_set
        installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
        
        self.cwd_is_writable = isWritable(os.getcwd())
        self.root_filesystem = get_fs_type("/")
        self.number_of_vars_in_env = len(os.environ.items())
        self.invocation_dir = os.getcwd()
        self.path_to_core = Path(__file__)
        self.running_in_venv = in_venv()
        self.path_to_venv = os.environ['VIRTUAL_ENV']
        self.python_version = platform.python_version()
        self.python_details = sys.version
        self.number_of_installed_python_packages = len(installed_packages_list)
        self.platform = platform.platform()
        self.distro = platform.freedesktop_os_release()["PRETTY_NAME"]

appcontext = AppContext()

def initapp():
    setup_workingset()

    from texttable import Texttable
    t = Texttable()
    t.add_rows([['check', 'result'], 
        ['cwd is writable', appcontext.cwd_is_writable], 
        ['root filesystem', appcontext.root_filesystem],
        ['number of vars in env', appcontext.number_of_vars_in_env],
        ['invocation dir', appcontext.invocation_dir],
        ['path to core', appcontext.path_to_core],
        ['running in venv', appcontext.running_in_venv],
        ['path to venv', appcontext.path_to_venv],
        ['python version', appcontext.python_version],
        ['python details', appcontext.python_details],
        ['number of installed python packages', appcontext.number_of_installed_python_packages],
        ['platform', appcontext.platform],
        ['distro', appcontext.distro]
    ])
    print(t.draw())
    
    import pipes
    print(sys.argv[0], ' '.join( [pipes.quote(s) for s in sys.argv[1:]] ))
    #print(psutil.Process().memory_info().rss / (1024 * 1024))
    #print(psutil.virtual_memory().percent)
    #print(platform.freedesktop_os_release())
