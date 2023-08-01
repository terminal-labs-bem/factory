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

from . import settings
from . import app

import click

context_settings = {"help_option_names": ["-h", "--help"]}

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

@plugins_group.command(name="use")
def usetplugins_command():
    #plugins = Plugins("simple")
    #plugins.run()
    plugins = ComplexPlugins("complex")
    plugins.run({"123": "abc"})

def dl_zip(url, name, workingdir):
    if not exists(workingdir + name):
        with urlopen(url) as response, open(workingdir + name, "wb") as out_file:
            shutil.copyfileobj(response, out_file)

def unzip(source, extract):
    with ZipFile(source) as zf:
        zf.extractall(path=extract)

def _delete_dir(directory):
    directory = abspath(directory)
    if exists(directory):
        shutil.rmtree(directory)

def _copy_dir(source, target):
    if not exists(target):
        shutil.copytree(abspath(source), abspath(target))

def _rename_dir(source, target):
    os.rename(source, target)

def _fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(_fast_scandir(dirname))
    return subfolders


def _fast_scandfiles(dirname):
    dirs = _fast_scandir(dirname)
    files = [f.path for f in os.scandir(dirname) if f.is_file()]
    for dir in dirs:
        files.extend([f.path for f in os.scandir(dir) if f.is_file()])
    return files

from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

from tempfile import mkstemp
from shutil import move
from os import remove

def _replace(source_file_path, pattern, substring):
    fh, target_file_path = mkstemp()
    with open(target_file_path, 'w') as target_file:
        with open(source_file_path, 'r') as source_file:
            for line in source_file:
                target_file.write(line.replace(pattern, substring))
    remove(source_file_path)
    move(target_file_path, source_file_path)

def modify_repo(path, oldname, newname):
    last_cwd = os.getcwd()
    os.chdir(path)

    import toml

    input_file_name = ".repo/rules.toml"
    with open(input_file_name) as toml_file:
        toml_dict = toml.load(toml_file)

    rules = toml_dict
    renamedirs = rules["renamedirs"]
    editlines = rules["editlines"]

    abs_renamedirs = []
    for renamedir in renamedirs:
        renamedir = renamedir.replace("[repo]", path)
        abs_renamedirs.append(os.path.abspath(renamedir))

    abs_editlines = []
    for editline in editlines:
        editline[0] = os.path.abspath(editline[0].replace("[repo]", path))
        editline[1] = editline[1].replace("[oldname]", oldname)
        editline[2] = editline[2].replace("[newname]", newname)
        abs_editlines.append(editline)

    dirs = _fast_scandir(path)
    abs_dirs = []
    for dir in dirs:
        abs_dirs.append(os.path.abspath(dir))

    files = _fast_scandfiles(path)
    abs_files = []
    for f in files:
        abs_files.append(os.path.abspath(f))       

    for dir in abs_dirs:
        if dir in  abs_renamedirs:
            _rename_dir(dir, os.path.dirname(dir) + "/" + newname)

    for f in abs_editlines:
        print(f)
        print(abs_editlines)
        if f in abs_editlines:
            print("got no")
            _replace(f[0],f[1],f[2])

    os.chdir(last_cwd)
    # toml_string = toml.dumps(toml_dict)
    # print(toml_string)


@plugins_group.command(name="clone")
def usetplugins_command():
    print("time to clone")
    plugins = Plugins("default")
    plugins.run()

@click.option('-n', '--name', 'name')
@builtin_group.command("dlself")
def builtin_dlself_cmd(name):
    if name:
        filename = name
    else:
        filename = "factory_pilot-main"
    dl_zip("https://github.com/terminal-labs/factory_pilot/archive/refs/heads/main.zip", "factory_pilot-main.zip", ".tmp/storage/download/")
    unzip(".tmp/storage/download/factory_pilot-main.zip", ".tmp/storage/unzipped")
    _copy_dir(".tmp/storage/unzipped/factory_pilot-main", ".tmp/temporary/factory_pilot-main")
    modify_repo(os.path.abspath(".tmp/temporary/factory_pilot-main"), "factory", "factory5")
    _copy_dir(".tmp/temporary/factory_pilot-main", name)
    _delete_dir(os.path.abspath(".tmp/temporary/factory_pilot-main"))


cli.add_command(builtin_group)
cli.add_command(plugins_group)
