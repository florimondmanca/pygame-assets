"""Testing utilities."""

import unittest
from contextlib import contextmanager
from pygame_assets.configure import set_environ_config, Config, get_config, \
    remove_config
from pygame_assets import core


class TestConfig(Config):
    """Configuration for tests.

    Redefines the base assets directory.
    """

    name = 'test'

    class Meta:  # noqa
        base = 'tests/assets'


class TestCase(unittest.TestCase):
    """Test case suited for tests that load test assets.

    Adds setUp and tearDown steps to look for test assets in tests/assets.
    """

    def setUp(self):
        set_environ_config('test')

    def tearDown(self):
        set_environ_config(None)


@contextmanager
def define_test_text_loader():
    """Utility context manager.

    1. Creates a text loader which gets registered to pygame_assets,
    2. Yields the loader,
    3. Cleans up by unregistering the loader from pygame_assets.
    """
    @core.loader(name='text')
    def load_text(filepath):
        with open(filepath, 'r') as textfile:
            text = textfile.read()
        return text
    yield load_text
    core.unregister('text')


@contextmanager
def change_config(*attributes, config=None):
    """Utility context manager.

    Use when you are writing an attribute of the config returned by
    get_config(). It ensures that the attribute will be kept the same
    before and after the write -- useful to keep tests independant.

    Example
    -------
    ```
    with change_config('default_setting') as config:
        config.default_setting = 'foo'
        # do some asserts...
    # now the value of config.default_setting is not 'foo' anymore.
    ```

    Returns
    -------
    config : Config

    Parameters
    ----------
    *attributes : list of str
        The names of the config attributes that are going to be written during
        tests.
    config : Config, optional, kwarg only.
        You can pass a config object to use, default behavior is to
        use get_config().

    """
    if config is None:
        config = get_config()
    old_values = {attr: getattr(config, attr) for attr in attributes}
    try:
        yield config
    finally:
        for attr, old_value in old_values.items():
            setattr(config, attr, old_value)


@contextmanager
def temp_config(*names):
    """Utility context manager.

    Use when declaring a new configuration to prevent from polluting the
    global configuration manager.

    Example
    -------
    ```
    with temp_config('custom'):
        class CustomConfig(Config):
            name = 'custom'
    # now the config 'custom' does not exist anymore.
    ```

    Parameters
    ----------
    names : list of str
        The list of config names that are going to be declared.

    """
    try:
        yield
    finally:
        for name in names:
            remove_config(name)
