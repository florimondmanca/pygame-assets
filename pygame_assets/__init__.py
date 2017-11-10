from .project_config import config
from . import loaders
from .core import _loaders_list

config.add_default_dirs(_loaders_list)

load = loaders.FunctionLoadersIndex(loaders.load_functions)


def init():
    """Initialize the pygame-assets package.

    Typically called after changing config settings such as
    the custom loaders module.
    """
    # register loaders from a local assets.py file

    try:
        import imp
        fp, name, description = imp.find_module(config.custom_loaders_module)
        try:
            imp.load_module(config.custom_loaders_module, fp, name, description)
        except ImportError:
            fp.close()
    except ImportError:
        pass


init()
