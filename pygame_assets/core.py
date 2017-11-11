"""The core loader.

Provides basic asset loading workflow, with error management and
conversion to a plain function.
"""
import pygame
from .exceptions import AssetNotFoundError, InvalidAssetLoaderNameError
from .configure import get_config


class AssetLoaderMeta(type):
    """Metaclass for AssetLoader.

    Defines a default asset_type class attribute at class initialization.
    """

    def __init__(cls, name, base, namespace):
        super().__init__(name, base, namespace)

        # assign the asset_type attribute to the cls
        asset_type = namespace.get('asset_type')
        if not asset_type:
            asset_type = AssetLoaderMeta.get_asset_type(name)
        cls.asset_type = asset_type

        if cls.asset_type != 'asset':
            # create the config default search dir for newly
            # created loader class
            get_config().add_default_dir(cls)

    def get_asset_type(name):
        if 'loader' not in name.lower():
            raise InvalidAssetLoaderNameError(name)
        return name.lower().replace('loader', '')


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
        search_paths = get_config().search_paths(self.asset_type, filename)
        for filepath in search_paths:
            try:
                asset = self.get_asset(filepath, *args, **kwargs)
                return asset
            except (pygame.error, FileNotFoundError):
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

        The class's get_asset() method documentation is copied to
        the return function loader.

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

        load_asset.__doc__ = cls.get_asset.__doc__

        return load_asset
