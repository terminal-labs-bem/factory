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


from . initialization.helpers import modify_repo

def find_plugins(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

def main():
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


def list_projects():
    html_url = "https://github.com/orgs/terminal-labs-bem/repositories"
    response = requests.get(html_url).content
    soup = bs.BeautifulSoup(response, "lxml")

    repos = []
    for tag in soup.find_all("a"):
        if "nib_" in str(tag.attrs["href"]):
            repos.append(tag.attrs["href"])
    repos = sorted(repos)

    repo_groups = []
    for group in range(int(len(repos) / 3)):
        repo_groups.append([repos.pop(0) for _ in range(3)])

    repo_names = []
    for repo_group in repo_groups:
        repo_names.append(repo_group[0].split("/")[-1])
    return repo_names


def init_project(cwd, project, name):
    urllib.request.urlretrieve(
        "https://github.com/terminal-labs-bem/" + project + "/archive/refs/heads/main.zip",
        ".tmp/storage/download/" + project + ".zip",
    )

    with zipfile.ZipFile(".tmp/storage/download/" + project + ".zip", "r") as zip_ref:
        zip_ref.extractall(".tmp/storage/unzipped")
    modify_repo(
        cwd + "/.tmp/storage/unzipped/" + project + "-main",
        "simplenib",
        "lxc",
    )
