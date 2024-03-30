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

import toml

from lowkit.utils import _fast_scandir, _fast_scandfiles, _replace_many_lines, _rename_dir

def new_repo_from_template(path, oldname, newname):
    def replace_term(filename, oldname, newname):
        with open(filename, 'r') as file:
            filedata = file.read()
        filedata = filedata.replace(oldname, newname)
        with open(filename, 'w') as file:
            file.write(filedata)     

    last_cwd = os.getcwd()
    os.chdir(path)

    input_file_name = ".repo/rules.toml"
    with open(input_file_name) as toml_file:
        toml_dict = toml.load(toml_file)

    rules = toml_dict

    renamedirs = rules["renamedirs"]
    editlines = rules["editlines"]
    inherited = rules["inherited"]
    termsynced = rules["termsynced"]

    replace_term('setup.cfg', oldname, newname)
    replace_term('setup.py', oldname, newname)
    replace_term('tests/test_cmd_info.py', oldname, newname)

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
        if dir in abs_renamedirs:
            _rename_dir(dir, os.path.dirname(dir) + "/" + newname)

    edit_directives = []
    for f in abs_editlines:
        edit_directives.append([f[0], [f[1], f[2]]])

    files = []
    groups = {}
    for edit_directive in edit_directives:
        if edit_directive[0] not in files:
            files.append(edit_directive[0])
        if edit_directive[0] not in groups.keys():
            groups[edit_directive[0]] = [edit_directive[1]]
        else:
            groups[edit_directive[0]].append(edit_directive[1])

    for key in groups.keys():
        _replace_many_lines(key, groups[key])

    os.chdir(last_cwd)