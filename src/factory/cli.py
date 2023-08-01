import os
import sys
from os import listdir
from os.path import isfile, join
import importlib
import importlib.util

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

@click.group(name="app")
def app_group():
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

@plugins_group.command(name="clone")
def usetplugins_command():
    plugins = Plugins("default")
    plugins.run()

@app_group.command("main")
def app_main_cmd():
    app.main()

cli.add_command(app_group)
cli.add_command(plugins_group)
