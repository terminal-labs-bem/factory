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

def find_plugins(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

class Plugin:
    def process(self):
        print("using default plugin")
        print(f"Numbers are {num1} and {num2}")

class ComplexPlugin:
    def process(self):
        print("using default plugin")
        print(f"Numbers are {num1} and {num2}")

class Plugins:
    def __init__(self, plugin):
        cwd = os.getcwd()
        if plugin + ".py" in find_plugins(cwd + "/plugins"):
            spec = importlib.util.spec_from_file_location('default',cwd + "/plugins/" + plugin + ".py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self._plugin = module.Plugin()
        else:
            self._plugin = Plugin()

    def run(self):
        cwd = os.getcwd()
        self._plugin.process()

class ComplexPlugins:
    def __init__(self, plugin):
        cwd = os.getcwd()
        if plugin + ".py" in find_plugins(cwd + "/plugins"):
            spec = importlib.util.spec_from_file_location('default',cwd + "/plugins/" + plugin + ".py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self._plugin = module.Plugin()
        else:
            self._plugin = Plugin()

    def run(self, data):
        cwd = os.getcwd()
        self._plugin.process(data)
