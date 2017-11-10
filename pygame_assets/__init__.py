from .core import config
from . import loaders
from .loaders import load


def init():
    """Initialize the pygame-assets package.

    Typically called after changing config settings such as
    the custom loaders module.
    """
    # register custom loades
    try:
        import imp
        fp, name, description = imp.find_module(config.custom_loaders_location)
        try:
            imp.load_module(config.custom_loaders_location,
                            fp, name, description)
        except ImportError:
            fp.close()
    except ImportError:
        pass


init()
