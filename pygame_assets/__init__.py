from .project_config import config
from . import loaders
from .core import _loaders_list

config.add_default_dirs(_loaders_list)

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


class FunctionLoadersIndex:
    """When instanciated, allows to access function loaders by attribute."""

    def __getattr__(self, name):
        loader = loaders.load_functions.get(name)
        if loader is not None:
            return loader
        else:
            raise AttributeError('No such loader: {}'.format(name))


load = FunctionLoadersIndex()
