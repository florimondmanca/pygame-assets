from .project_config import config
from .loaders import *
from .core import _loaders_list

config.add_default_dirs(_loaders_list)
