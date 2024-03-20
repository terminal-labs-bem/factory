import os
import urllib.request
import zipfile
import os
import sys
from os import listdir
from os.path import isfile, join
import importlib
import importlib.util
import os
import shutil
import urllib
import subprocess
from urllib.request import urlopen
from os.path import isdir, dirname, realpath, abspath, join, exists
from zipfile import ZipFile
from configparser import ConfigParser

import requests
import bs4 as bs


from lowkit.initialization.helpers import modify_repo
from lowkit.initialization.workingset import setup_workingset

def find_plugins(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

def main():
    setup_workingset()
    pass


def list_plugins():
    cwd = os.getcwd()
    print(find_plugins(cwd + "/plugins"))


def use_plugin():
    optsdict = {}
    opts = data.split(",")
    for opt in opts:
        pair = opt.split(":")
        optsdict[pair[0]] = pair[1]
    plugins = ComplexPlugins(plugin)
    plugins.run({"cmd": command, "name": optsdict["destination"]})



def init_project(cwd, name):
    project = "template"
    urllib.request.urlretrieve(
        "https://github.com/terminal-labs-bem/" + project + "/archive/refs/heads/main.zip",
        ".tmp/storage/download/" + project + ".zip",
    )

    with zipfile.ZipFile(".tmp/storage/download/" + project + ".zip", "r") as zip_ref:
        zip_ref.extractall(".tmp/storage/unzipped")
    modify_repo(
        cwd + "/.tmp/storage/unzipped/" + project + "-main",
        project,
        name,
    )
    from lowkit.utils import _copy_dir, _delete_dir
    _copy_dir(cwd + "/.tmp/storage/unzipped/" + project + "-main", name)
    _delete_dir(cwd + "/.tmp/storage/unzipped/" + project + "-main")
