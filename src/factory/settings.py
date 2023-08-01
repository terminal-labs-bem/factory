import os.path
from importlib.metadata import version

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_NAME = os.path.basename(PROJECT_ROOT)
PROJECTNAME = PROJECT_NAME.replace("_", "").replace("-", "")
VERSION = version(PROJECT_NAME)