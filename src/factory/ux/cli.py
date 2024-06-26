import os

from .. import settings
from .. import app

import click

context_settings = {"help_option_names": ["-h", "--help"]}


def init():
    app.main()


@click.group(context_settings=context_settings)
@click.version_option(
    prog_name=settings.PROJECT_NAME.capitalize(), version=settings.VERSION
)
@click.pass_context
def cli(ctx):
    init()


@click.group(name="plugins")
def plugins_group():
    pass


@click.group(name="builtin")
def builtin_group():
    pass


@plugins_group.command(name="listplugins")
def listplugins_command():
    app.list_plugins()


@click.option("-p", "--plugin", "plugin")
@click.option("-c", "--command", "command")
@click.option("-d", "--data", "data")
@plugins_group.command(name="useplugin")
def useplugin_command(plugin, command, data):
    app.use_plugin()


@click.option("-n", "--name", "name")
@builtin_group.command("initproject")
def builtin_initproject_cmd(name):
    cwd = os.getcwd()
    app.init_project(cwd, name)


@click.option("-n", "--name", "name")
@builtin_group.command("updateproject")
def builtin_updateproject_cmd(name):
    cwd = os.getcwd()
    app.update_project(cwd, name)


cli.add_command(builtin_group)
