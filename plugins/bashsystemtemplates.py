import os
import sys

from lowkit.utils import _delete_dir, _copy_dir
from lowkit.functions.helpers import dl_zip, unzip
from lowkit.functions.helpers import modify_repo
from lowkit.utils import _delete_dir, _fast_scandir_shallow

def process_gh_link(url, newname):
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

class Plugin:
    def process(self, data):
        print("This is my simple plugin")
        print(data)

        newname = data["name"]
        url = "https://github.com/terminal-labs/factory_pilot/archive/refs/heads/main.zip"
        process_gh_link(url, newname)