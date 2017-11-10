"""The core loader.

Provides basic asset loading workflow, with error management and
conversion to a plain function.
"""

import os
import pygame
from exceptions import AssetNotFoundError


class AssetLoaderMeta(type):
    """Metaclass for AssetLoader.

    Defines a default asset_type class attribute at class initialization.
    """

    UNDEFINED_ASSET_TYPE = 'undefined'

    def __init__(cls, name, base, namespace):
        asset_type = namespace.get('asset_type')
        if not asset_type:
            asset_type = AssetLoaderMeta.get_asset_type(name)
        cls.asset_type = asset_type

    def get_asset_type(name):
        if 'loader' in name.lower():
            return name.lower().replace('loader', '')
        else:
            return AssetLoaderMeta.UNDEFINED_ASSET_TYPE


def get_default_base_dir():
    """# TODO."""
    return ''


class AssetLoader(metaclass=AssetLoaderMeta):
    """Base asset loader.

    Exposes a load(filename, *args, **kwargs) that shall be implemented in
    inherited assets.

    Class attributes
    ----------------
    asset_type : str
        The type of asset this loader supports.
        A default value based on the class's name is defined at definition.
    search_dirs : list of str
        The directories where this loader searches assets, relative
        to the base_dir.
    base_dir : str
        The base directory for asset search. Default is the empty string.
    """

    search_dirs = ['']  # TODO

    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = get_default_base_dir()
        self._base_dir = base_dir

    @property
    def base_dir(self):
        return self._base_dir

    def load(self, filename, *args, **kwargs):
        """Load an asset.

        Parameters
        ----------
        filename : str
            The asset's filename, e.g. 'my-image.png'.
        """
        for search_dir in self.search_dirs:
            file_path = self.get_file_path(search_dir, filename)
            try:
                asset = self.get_asset(file_path, *args, **kwargs)
                return asset
            except pygame.error as e:
                pass
        raise AssetNotFoundError(filename)

    def get_asset(self, file_path, *args, **kwargs):
        """Get the asset given a full file path.

        Abstract class method, shall be implemented in subclasses using
        pygame's assets.

        Parameters
        ----------
        file_path : str
            Full path to the asset.
        """
        raise NotImplementedError

    def get_file_path(self, search_dir, filename):
        # TODO
        return os.path.join(self.base_dir, search_dir, filename)

    @classmethod
    def as_function(cls, returned=lambda asset: asset):
        """Build and return the function loader.

        A function loader has the following signature :

        loader(filename, *args, **kwargs) -> asset

        The *args and **kwargs get transferred to the
        class's get_asset(filepath, *args, **kwargs) function.

        Parameters
        ----------
        returned : function, optional
            The result of this function is returned by the
            loader function.
            It must take the loaded asset as its only parameter.
            The default returns the asset itself.
        """
        def load_asset(filename, *args, **kwargs):
            loader = cls(**kwargs)
            asset = loader.load(filename, *args, **kwargs)
            return returned(asset)

        load_asset.__doc__ = "Load a {}.".format(cls.asset_type)

        return load_asset
