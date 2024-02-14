import os


def setup_workingset():
    dottmpdirs = [
        ".tmp",
        ".tmp/storage",
        ".tmp/storage/artifact",
        ".tmp/storage/auth",
        ".tmp/storage/bin",
        ".tmp/storage/clone",
        ".tmp/storage/data",
        ".tmp/storage/download",
        ".tmp/storage/repo",
        ".tmp/storage/scratch",
        ".tmp/storage/script",
        ".tmp/storage/unzipped",
    ]

    for dir in dottmpdirs:
        if not os.path.exists(dir):
            os.mkdir(dir)
