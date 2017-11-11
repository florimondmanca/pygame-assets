"""Per-project configuration API."""
import os


_CONFIG_ENV_VAR = 'PYGAME_ASSETS_CONFIG'
CONFIGS = {}


class ConfigMeta(type):
    """Config metaclass.

    Simply registers configuration classes to the configs dictionary.
    """

    def __init__(cls, name, base, namespace):
        super().__init__(name, base, namespace)

        config_name = namespace.get('name')
        CONFIGS[config_name] = cls


class Config(metaclass=ConfigMeta):
    """Config object that allows project-specific configuration."""

    name = 'default'
    base = 'assets'
    custom_loaders_location = 'custom_loaders'
    dirs = {}

    @classmethod
    def add_default_dir(cls, loader_class):
        """Add the default directory for a loader class to the config."""
        asset_type = loader_class.asset_type
        if asset_type not in cls.dirs:
            cls.dirs[asset_type] = [asset_type]

    @classmethod
    def search_dirs(cls, asset_type):
        """Return directories where to search assets of this type.

        Returned as a generator.

        Parameters
        ----------
        asset_type : str
        """
        dirs = cls.dirs.get(asset_type, [asset_type])
        return (os.path.join(cls.base, dir_) for dir_ in dirs)

    @classmethod
    def search_paths(cls, asset_type, filename):
        """Return file paths where to search this asset.

        Returned as a generator.

        Parameters
        ----------
        asset_type : str
        filename : str
        """
        search_dirs = cls.search_dirs(asset_type)
        return (os.path.join(dir_, filename) for dir_ in search_dirs)

    def __str__(self):
        # TODO print the config's parameters
        return super().__str__()


class TestConfig(Config):
    """Config for tests."""

    name = 'test'
    base = 'tests/assets'


def get_config(name=None):
    """Return a config.

    Parameters
    ----------
    name : str
        The name of the wanted config object. Can be 'default' or 'test'.
        Note: if None (the default), environment variable PYGAME_ASSETS_CONFIG
        will be used. If not defined, the default config will be returned.
    """
    if name is None:
        name = os.environ.get(_CONFIG_ENV_VAR, 'default')
    return CONFIGS[name]


def set_environ_config(name=None):
    """Set the config environment variable.

    If name is None, clear the config environment variable.
    """
    if name:
        os.environ.setdefault(_CONFIG_ENV_VAR, name)
    else:
        os.environ.pop(_CONFIG_ENV_VAR)
