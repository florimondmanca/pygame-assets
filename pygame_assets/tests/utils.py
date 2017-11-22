"""Testing utilities."""

import unittest
from contextlib import contextmanager
from pygame_assets.configure import set_environ_config, Config, get_config
from pygame_assets import core


class TestConfig(Config):
    """Configuration for tests.

    Redefines the base assets directory.
    """

    name = 'test'
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
def define_test_loader(name):
    """Utility context manager.

    1. Creates a text loader which gets registered to pygame_assets,
    2. Yields the loader,
    3. Cleans up by unregistering the loader from pygame_assets.
    """
    @core.loader(name=name)
    def load_text(filepath):
        with open(filepath, 'r') as textfile:
            text = textfile.read()
        return text
    yield load_text
    core.unregister(name)


@contextmanager
def change_config(attr_name, config=None):
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
    attr_name : str
        The name of the config attribute that is going to be written during
        tests.
    config : Config, optional
        You can pass a config object to use, default behavior is to
        use get_config().

    """
    if config is None:
        config = get_config()
    old_value = getattr(config, attr_name)
    try:
        yield config
    finally:
        setattr(config, attr_name, old_value)
