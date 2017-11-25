"""Per-project configuration API."""
import os
from .exceptions import NoSuchConfigurationParameterError


_CONFIG_ENV_VAR = 'PYGAME_ASSETS_CONFIG'

# TODO turn into a ConfigsManager to make it more easily testable
CONFIGS = {}


class ConfigMeta(type):
    """Metaclass for Config objects.

    Build the _meta config instance dictionary using the class' Meta
    inner class.
    The Meta inner class is where all the configuration parameters
    are defined.
    Registers configuration classes to the configure.CONFIGS dict.
    """

    _allowed_params = (
        'base',
        'default_font_size',
        'custom_loaders_location',
    )

    def __new__(meta, name, bases, namespace):
        # the declared config must have a name
        config_name = namespace.get('name')
        if not config_name:
            raise ValueError('Config classes must have '
                             'a name attribute, none was found.')

        # build the _meta dict from the inner Meta class
        meta_cls = namespace.pop('Meta', None)
        namespace['_meta'] = meta.create_meta(meta_cls, bases)

        return super().__new__(meta, name, bases, namespace)

    def __init__(cls, name, base, namespace):
        super().__init__(name, base, namespace)
        # register instance of the config class
        CONFIGS[cls.name] = cls()

    @classmethod
    def create_meta(meta, meta_cls, bases):
        _meta = {}
        if bases:
            base = bases[0]
            _meta.update(base._meta)
        proper_meta = meta.get_class_attributes(meta_cls)
        _meta.update(proper_meta)
        for param_name, param_value in _meta.items():
            if param_name not in ConfigMeta._allowed_params:
                raise NoSuchConfigurationParameterError(param_name)
        return _meta

    def get_class_attributes(cls):
        """Return class attributes of a class.

        Disregards functions and built-in class attributes.
        """
        if cls:
            return {
                key: value
                for key, value in cls.__dict__.items()
                if not key.startswith('__') and not callable(value)
            }
        return {}


class Config(metaclass=ConfigMeta):
    """Config object that allows project-specific configuration."""

    name = 'default'
    dirs = {}

    class Meta:
        """Define here all configuration parameters."""

        base = './assets'
        default_font_size = 20
        custom_loaders_location = 'asset_loaders'

    def __getattr__(self, name):
        try:
            return self._meta[name]
        except KeyError:
            return self.__getattribute__(name)

    def __eq__(self, other):
        return all([
            self.name == other.name,
            self.dirs == other.dirs,
            self._meta == other._meta,
        ])

    def add_search_dirs(self, loader_name, *search_dirs):
        """Register search directories for a loader.

        Parameters
        ----------
        loader_name : str
        *search_dirs : list of str, optional
            The list of directories this loader will search into.
        """
        self.dirs.setdefault(loader_name, [])
        for default_dir in search_dirs:
            self.dirs[loader_name].append(default_dir)

    def remove_search_dirs(self, loader_name):
        """Remove search directories for a loader.

        Parameters
        ----------
        loader_name : str
        """
        self.dirs.pop(loader_name)

    def search_dirs(self, loader_name):
        """Return directories where a loader will search for assets.

        Parameters
        ----------
        loader_name : str
        """
        dirs = self.dirs[loader_name]
        return [os.path.join(self.base, dir_) for dir_ in dirs]

    def search_paths(self, loader_name, filename):
        """Return file paths where a loader will search an asset.

        Parameters
        ----------
        loader_name : str
        filename : str
        """
        search_dirs = self.search_dirs(loader_name)
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


def config_exists(name):
    """Return whether a config exists.

    Parameters
    ----------
    name : str
    """
    return name in CONFIGS


def remove_config(name):
    """Safely remove a registered configuration.

    Has no effect if the configuration does not exist.

    Parameters
    ----------
    name : str
    """
    CONFIGS.pop(name, None)


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
