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
    base = './assets'
    custom_loaders_location = 'asset_loaders'
    dirs = {}

    @classmethod
    def add_default_dir(cls, loader_name):
        """Add the default directory for a given loader name to the config."""
        cls.dirs.setdefault(loader_name, [loader_name])

    @classmethod
    def remove_dirs(cls, loader_name):
        """Remove search directories for a loader."""
        cls.dirs.pop(loader_name)

    @classmethod
    def search_dirs(cls, loader_name):
        """Return directories where a loader will search for assets.

        Parameters
        ----------
        loader_name : str
        """
        dirs = cls.dirs[loader_name]
        return [os.path.join(cls.base, dir_) for dir_ in dirs]

    @classmethod
    def search_paths(cls, loader_name, filename):
        """Return file paths where a loader will search an asset.

        Parameters
        ----------
        loader_name : str
        filename : str
        """
        search_dirs = cls.search_dirs(loader_name)
        return [os.path.join(dir_, filename) for dir_ in search_dirs]

    def __str__(self):
        # TODO print the config's parameters
        return super().__str__()


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
        name = get_environ_config() or 'default'
    return CONFIGS[name]


def get_environ_config():
    """Get the config name from the shell environment.

    If not defined, return None.
    """
    return os.environ.get(_CONFIG_ENV_VAR, None)


def set_environ_config(name):
    """Set the config environment variable.

    If name is None, clear the config environment variable.
    """
    if name is None:
        try:
            del os.environ[_CONFIG_ENV_VAR]
        except KeyError:
            pass
    else:
        os.environ.setdefault(_CONFIG_ENV_VAR, name)
