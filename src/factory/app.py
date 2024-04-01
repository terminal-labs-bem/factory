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

from lowkit.utils import _copy_dir, _delete_dir
from factory.core import initapp
from factory.ops.repomanipulation import (
    new_repo_from_template,
    update_repo_from_template,
    get_repo_filepath_objs,
    copy_new_files,
    get_rules,
    replace_term,
)

from . import settings


def main():
    initapp()


def info():
    return settings.PROJECT_ROOT


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
        "https://github.com/terminal-labs-bem/"
        + project
        + "/archive/refs/heads/main.zip",
        ".tmp/storage/download/" + project + ".zip",
    )

    with zipfile.ZipFile(".tmp/storage/download/" + project + ".zip", "r") as zip_ref:
        zip_ref.extractall(".tmp/storage/unzipped")
    new_repo_from_template(
        cwd + "/.tmp/storage/unzipped/" + project + "-main",
        project,
        name,
    )

    _copy_dir(cwd + "/.tmp/storage/unzipped/" + project + "-main", name)
    _delete_dir(cwd + "/.tmp/storage/unzipped/" + project + "-main")


def update_project(cwd, name):
    project = "template"
    urllib.request.urlretrieve(
        "https://github.com/terminal-labs-bem/"
        + project
        + "/archive/refs/heads/main.zip",
        ".tmp/storage/download/" + project + ".zip",
    )

    with zipfile.ZipFile(".tmp/storage/download/" + project + ".zip", "r") as zip_ref:
        zip_ref.extractall(".tmp/storage/unzipped")

    templatepath = cwd + "/.tmp/storage/unzipped/" + project + "-main"
    template_objects = get_repo_filepath_objs(templatepath)
    template_repo_files = [f.pathfrom for f in template_objects]
    normalized_template_repo_files = [
        f.replace("warehouse", "template") for f in template_repo_files
    ]

    projectpath = cwd + "/" + name
    project_objects = get_repo_filepath_objs(projectpath)
    project_repo_files = [f.pathfrom for f in project_objects]
    normalized_project_repo_files = [
        f.replace("warehouse", "template") for f in project_repo_files
    ]

    copy_new_files(
        project,
        name,
        templatepath,
        projectpath,
        set(normalized_template_repo_files) - set(normalized_project_repo_files),
    )

    rules = get_rules(projectpath)
    inherited = rules["inherited"]
    for i in inherited:
        oldpath = templatepath + "/" + i.replace(name, project)
        newpath = projectpath + "/" + i
        os.makedirs(os.path.dirname(newpath), exist_ok=True)
        shutil.copyfile(oldpath, newpath)

    semiinherited = rules["semiinherited"]
    for s in semiinherited:
        oldpath = templatepath + "/" + s
        newpath = projectpath + "/" + s
        os.makedirs(os.path.dirname(newpath), exist_ok=True)
        shutil.copyfile(oldpath, newpath)
        replace_term(newpath, project, name)
