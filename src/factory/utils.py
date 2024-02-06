import os
import sys
import time
import json
import yaml
import shutil
import hashlib
import zipfile
import base64
import uuid
from pathlib import Path


def test():
    return getconfig()


def remove(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        if os.path.isdir(path):
            shutil.rmtree(path)


def create_dirs(dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.mkdir(dir)


def init_runner_env():
    create_dirs(tmp_dirs)
    dir = ".tmp/runners/"
    if not os.path.exists(dir):
        os.mkdir(dir)

    dir = ".tmp/runners/runs"
    if not os.path.exists(dir):
        os.mkdir(dir)


import configparser
from pathlib import Path
from os.path import abspath, isfile, dirname, islink, isdir
from os import walk, symlink, listdir, path

config = configparser.ConfigParser()

package_link = ".tmp/symlink"
_setuppy = "/setup.py"
_setupcfg = "/setup.cfg"
_dsstore = ".DS_Store"
_repo = "repo"
_back = ".."
_blank = ""
_slash = "/"
_path = str(Path(__file__).parent.absolute())
_src = ""


def cwd():
    return path.join(dirname(__file__))


def join(*args):
    return abspath(path.join(*args))


def split(a):
    return a.split(_slash)


def backout(path):
    return join(path, _back)


def import_fun(mod, func):
    return getattr(__import__(mod, fromlist=[func]), func)


def get_pkg_dir():
    currentpath = cwd()
    i = len(currentpath.split(_slash))
    while i > 0:
        currentpath = join(currentpath, _back)
        if isfile(currentpath + _setuppy):
            return currentpath
            i = -1
        i = i - 1


def find_file(name, path):
    for root, dirs, files in walk(path):
        if name in files:
            return join(root, name)


def find_src_dir():
    currentpath = cwd()
    currentpath = currentpath.split(_slash)
    currentpath.reverse()
    build_new_path = False
    new_path = []
    for dir in currentpath:
        if dir == "src":
            build_new_path = True
        if build_new_path:
            new_path.append(dir)
    new_path.reverse()
    return "/".join(new_path)


def find_config_file():
    currentpath = cwd()
    currentpath = currentpath.split(_slash)
    currentpath.reverse()
    search = currentpath[:]
    for dir in currentpath:
        search.pop(0)
        candidate = search[:]
        candidate.reverse()
        if find_file("setup.cfg", "/".join(candidate)):
            return find_file("setup.cfg", "/".join(candidate))


def find_local_file():
    currentpath = cwd()
    currentpath = currentpath.split(_slash)
    currentpath.reverse()
    search = currentpath[:]
    for dir in currentpath:
        search.pop(0)
        candidate = search[:]
        candidate.reverse()
        if find_file("local.py", "/".join(candidate)):
            return find_file("local.py", "/".join(candidate))


def is_install_editable():
    if find_src_dir() == "":
        return False
    else:
        return True


def get_pkg_name():
    config.read(find_config_file())
    NAME = config["metadata"]["name"]
    return NAME


def setup_links(package_name):
    _link = package_link + _slash
    Path(_path + _slash + _link).mkdir(parents=True, exist_ok=True)
    if not islink(_path + _slash + _link + package_name):
        symlink(join(_path, _src), _path + _slash + _link + _slash + package_name)


def smart_reqs(repos, package_name):
    # styles = standalone, repo

    def _get_deploy_style():
        currentpath = _path
        for _ in range(len(split(currentpath))):
            currentpath = backout(currentpath)
            if isdir(currentpath + _slash + ".tmp" + _slash + _repo):
                return _repo

    if _get_deploy_style() == _repo:
        local_repos = listdir(join(_path, _back))
        if _dsstore in local_repos:
            local_repos.remove(_dsstore)
        if package_name in local_repos:
            local_repos.remove(package_name)
        for repo in local_repos:
            repos = [_ for _ in repos if not _.endswith(repo + ".git")]
        return repos
    return repos


import os
import json
import base64
import random
import string

from pathlib import Path
from shutil import copyfile, move, rmtree
from subprocess import Popen, PIPE


def b64encode(data):
    assert isinstance(data, bytes) is True
    return base64.b64encode(data)


def random_tag():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


def dir_exists(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    return os.path.isdir(path)


def dir_create(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)


def dir_delete(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    rmtree(path)


def file_delete(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    os.remove(path)


def file_read(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    file_obj = open(path, "rb")
    data = file_obj.read()
    file_obj.close()
    return data


def file_write(path, data):
    assert isinstance(path, str) is True
    assert isinstance(data, str) is True
    path = os.path.abspath(path)
    file_obj = open(path, "wb")
    file_obj.write(data.encode("utf-8"))
    file_obj.close()


def file_read_json(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    file_data = file_read(path)
    dic = json.loads(file_data)
    return dic


def file_copy(src, dst):
    assert isinstance(src, str) is True
    assert isinstance(dst, str) is True
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    copyfile(src, dst)


def file_rename(src, dst):
    assert isinstance(src, str) is True
    assert isinstance(dst, str) is True
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    os.rename(src, dst)


def file_move(src, dst):
    assert isinstance(src, str) is True
    assert isinstance(dst, str) is True
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    move(src, dst)


def get_user_home():
    return str(Path.home())


def get_env_variable(name):
    assert isinstance(name, str) is True
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def print_kv_pairs(dic):
    assert isinstance(dic, dict) is True
    for key in dic.keys():
        print(f"{key} =", dic[key])


def list_files(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    return [
        name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))
    ]  # noqa: E501


def list_file_paths(path):
    assert isinstance(path, str) is True
    path = os.path.abspath(path)
    file_paths = []
    for root, directories, filenames in os.walk(path):
        for filename in filenames:
            file_paths.append(os.path.abspath(os.path.join(root, filename)))
    return file_paths


def __realtime_call(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        line = line.decode("utf-8")
        if not line:
            break
        yield line


def call_ssh_generator(user, host, command):
    for line in __realtime_call(f"ssh {user}@{host} '{command}'"):
        if not line:
            break
        yield line


def call_ssh(user, host, command):
    result = []
    for line in __realtime_call(f"ssh {user}@{host} '{command}'"):
        result.append(line + "\n")
    result = "".join([str(x) for x in result])
    return result


def call_local_shell(command):
    result = []
    for line in __realtime_call(f"{command}"):
        result.append(line + "\n")
    result = "".join([str(x) for x in result])
    return result


def prettyprintdict(value, htchar="\t", lfchar="\n", indent=0):
    nlch = lfchar + htchar * (indent + 1)
    if type(value) is dict:
        items = [
            nlch
            + repr(key)
            + ": "
            + prettyprintdict(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        items = sorted(items)
        return "{%s}" % (",".join(items) + lfchar + htchar * indent).replace("'", '"')
    elif type(value) is list:
        items = [
            nlch + prettyprintdict(item, htchar, lfchar, indent + 1) for item in value
        ]
        items = sorted(items)
        return "[%s]" % (",".join(items) + lfchar + htchar * indent).replace("'", '"')
    elif type(value) is tuple:
        items = [
            nlch + prettyprintdict(item, htchar, lfchar, indent + 1) for item in value
        ]
        items = sorted(items)
        return "(%s)" % (",".join(items) + lfchar + htchar * indent).replace("'", '"')
    else:
        return repr(value).replace("'", '"')
