"""The core of pygame-assets."""
import os
from .exceptions import AssetNotFoundError
from .configure import get_config


# mapping of names to the corresponding loader.
loaders = {}


def register(name, asset_loader, returned=None):
    """Register a loader, making it available in pygame_assets.load.

    Parameters
    ----------
    name : str
        The loader's name.
    asset_loader : function
        An asset loader as returned by the pygame_assets.loader decorator.
    returned : function, optional
        Must take an asset as its only parameter and return the final
        loaded asset.
    """
    if returned is not None:
        def loader_with_returned(filename, *args, **kwargs):
            asset = asset_loader(filename, *args, **kwargs)
            return returned(asset)
        loaders[name] = loader_with_returned
    else:
        loaders[name] = asset_loader


def unregister(name, in_config=True):
    """Unregister a loader.

    Raises a KeyError if no loader called `name` exists.

    Parameters
    ----------
    name : str
        The name of the loader to unregister.
    in_config : bool, optional
        If True (the default), unregisters the loader from search
        directories in the config (as obtained by get_config()).
    """
    del loaders[name]
    if in_config:
        get_config().remove_dirs(name)


def loader(name=None):
    """Decorator to register a loader.

    The decorated function must take a filepath as its first argument.
    It can then have any other positional or keyword arguments.

    Unless explicitely passed, the loader's name will be the decorated
    function's name.

    Usage
    -----
    @loader()
    def image(filepath):
        # load an image and return it

    @loader(name='customfont')
    def font(filepath, size=20):
        # load a font of given size and return it

    Parameters
    ----------
    name : str
        The name of the loader.
    """
    def create_asset_loader(get_asset):
        loader_name = name or get_asset.__name__

        # register default search directory for the loader
        get_config().add_default_dir(loader_name)

        # build the asset loader using load()
        def asset_loader(filename, *args, **kwargs):
            search_paths = get_config().search_paths(loader_name, filename)
            asset = load_asset(get_asset, filename, search_paths,
                               *args, **kwargs)
            return asset

        register(loader_name, asset_loader)
        return asset_loader

    return create_asset_loader


def load_asset(get_asset, filename, search_paths, *args, **kwargs):
    """Core function to load an asset.

    This function tries to call get_asset on each of the search paths.
    If no asset was found, raises an AssetNotFoundError.

    Parameters
    ----------
    get_asset : function
        The function being decorated by pygame_assets.load.
    search_paths : list of str
        List of paths where the loader will search for the asset.
    filename : str
        The asset's filename.
    """
    for filepath in search_paths:
        if not os.path.isfile(filepath):
            continue
        try:
            return get_asset(filepath, *args, **kwargs)
        except FileNotFoundError:
            pass
    raise AssetNotFoundError(filename, search_paths)


class LoaderIndex:
    """Allow to access registered loaders by attribute."""

    def __getattr__(self, name):
        loader = loaders.get(name)
        if loader is None:
            raise AttributeError('No such loader: {}'.format(name))
        return loader


load = LoaderIndex()
