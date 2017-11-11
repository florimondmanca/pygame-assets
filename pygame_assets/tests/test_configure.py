"""Tests for the config API."""

import unittest

from pygame_assets.configure import get_config, Config, \
    set_environ_config, get_environ_config


class TestConfigure(unittest.TestCase):
    """Unit tests for the Config API."""

    def setUp(self):
        set_environ_config(None)

    def test_set_environ_config(self):
        set_environ_config(None)
        self.assertIsNone(get_environ_config())
        set_environ_config('foo')
        self.assertEqual('foo', get_environ_config())

    def test_set_environ_config_is_explicit(self):
        with self.assertRaises(TypeError):
            set_environ_config()

    def test_load_default_config(self):
        explicit_config = get_config('default')
        self.assertEqual(explicit_config.name, 'default')
        no_args_config = get_config()
        self.assertEqual(no_args_config.name, 'default')

    def test_load_test_config(self):
        config = get_config('test')
        self.assertEqual(config.name, 'test')

    def test_get_config_from_env_var(self):
        class MyConfig(Config):
            name = 'myconfig'

        set_environ_config('myconfig')
        config = get_config()
        self.assertEqual('myconfig', config.name)

    def test_config_dirs_is_dict_of_loader_names_and_dirs(self):
        config = get_config()
        for loader_name, dirs in config.dirs.items():
            self.assertIsInstance(loader_name, str)
            self.assertIsInstance(dirs, list)
            self.assertIn(loader_name, dirs)

    def test_set_config_base(self):
        config = get_config()
        self.assertEqual('assets', config.base)
        config.base = 'static'
        self.assertEqual('static', config.base)
        # cleanup
        config.base = 'assets'

    def test_new_config_is_registered_to_get_config(self):
        # assert custom config does not exist already
        with self.assertRaises(KeyError):
            get_config('custom')

        class CustomConfig(Config):
            name = 'custom'
            base = 'custom/path/to/assets'

        # custom config should now be available through get_config()
        config = get_config('custom')
        self.assertEqual('custom', config.name)
        self.assertEqual('custom/path/to/assets', config.base)

    def test_search_dirs(self):
        config = get_config()
        config.base = 'assets'
        config.dirs['spritesheet'] = ['spritesheet', 'sheets']
        expected = ['assets/spritesheet', 'assets/sheets']
        actual = config.search_dirs('spritesheet')
        self.assertListEqual(expected, actual)
