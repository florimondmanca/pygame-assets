"""The core loader.

Provides basic asset loading workflow, with error management and
conversion to a plain function.
"""

import pygame
from .exceptions import AssetNotFoundError
from . import config


class AssetLoaderMeta(type):
    """Metaclass for AssetLoader.

    Defines a default asset_type class attribute at class initialization.
    """

    UNDEFINED_ASSET_TYPE = 'undefined'
    LOADERS = []  # all subclasses will end up in here

    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        # register the newly created loader class
        metacls.LOADERS.append(cls)
        return cls

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


class AssetLoader(metaclass=AssetLoaderMeta):
    """Base asset loader.

    Exposes a load(filename, *args, **kwargs) that shall be implemented in
    inherited assets.

    Class attributes
    ----------------
    asset_type : str
        The type of asset this loader supports.
        A default value based on the class's name is defined at definition.
        Note: pygame-assets will look for assets of this type in the
        asset_type subfolder of the configured base folder.
    """

    def load(self, filename, *args, **kwargs):
        """Load an asset.

        Parameters
        ----------
        filename : str
            The asset's filename, e.g. 'my-image.png'.
        """
        search_paths = config.search_paths(self.asset_type, filename)
        for filepath in search_paths:
            try:
                asset = self.get_asset(filepath, *args, **kwargs)
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


# Expose the list of loader classes
_loaders_list = AssetLoaderMeta.LOADERS
