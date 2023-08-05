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

from lowkit.utils import _delete_dir, _copy_dir
from lowkit.initialization.workingset import setup_workingset
from lowkit.functions.helpers import dl_zip, unzip

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

from . import settings
from . import app

import click

context_settings = {"help_option_names": ["-h", "--help"]}

def init():
    pass

@click.group(context_settings=context_settings)
@click.version_option(prog_name=settings.PROJECT_NAME.capitalize(), version=settings.VERSION)
@click.pass_context
def cli(ctx):
    pass

@click.group(name="builtin")
def builtin_group():
    pass

@click.group(name="plugins")
def plugins_group():
    pass

@plugins_group.command(name="listplugins")
def listplugins_command():
    cwd = os.getcwd()
    print(find_plugins(cwd + "/plugins"))

@click.option('-p', '--plugin', 'plugin')
@click.option('-c', '--command', 'command')
@click.option('-d', '--data', 'data')
@plugins_group.command(name="useplugin")
def usetplugins_command(plugin, command, data):
    optsdict = {}
    opts = data.split(",")
    for opt in opts:
        pair = opt.split(":")
        optsdict[pair[0]] = pair[1]
    plugins = ComplexPlugins(plugin)
    plugins.run({"cmd": command, "name": optsdict['destination']})

from lowkit.utils import _copy_dir
from lowkit.functions.helpers import modify_repo

@click.option('-n', '--name', 'name')
@builtin_group.command("selfreplicate")
def builtin_selfreplicate_cmd(name):
    newname = name
    url = "https://github.com/terminal-labs/factory_pilot/archive/refs/heads/main.zip"
    filename = "factory_pilot-main"
    storage_dir = ".tmp/storage/"
    dl_dir = storage_dir + "download/"
    unzipped_dir = storage_dir + "unzipped/"
    temporary_dir = ".tmp/temporary/" + filename
    
    dl_zip(url, filename + ".zip", dl_dir)
    unzip(dl_dir + filename + ".zip", unzipped_dir)
    _copy_dir(unzipped_dir + filename, temporary_dir)
    modify_repo(os.path.abspath(temporary_dir), "factory", newname)
    _copy_dir(temporary_dir, newname)
    _delete_dir(os.path.abspath(temporary_dir))


cli.add_command(builtin_group)
cli.add_command(plugins_group)
