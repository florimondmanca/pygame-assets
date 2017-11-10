"""The core loader."""

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
        The type of asset this loader supports. For debug purposes only.
    search_dirs : list of str
        The directories where this loader searches assets, relative
        to the base_dir.
    base_dir : str
        The base directory for asset search. Default is the empty string.
    """

    search_dirs = []

    def __init__(self, base_dir=None):
        if base_dir is None:
            base_dir = get_default_base_dir()
        self._base_dir = base_dir

    @property
    def base_dir(self):
        return self._base_dir

    def get_asset(self, file_path):
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
        return os.path.join(self.base_dir, search_dir, filename)

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
            except pygame.error as e:
                pass
            else:
                return asset
        raise AssetNotFoundError(filename)
