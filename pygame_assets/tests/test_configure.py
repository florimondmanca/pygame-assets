"""Tests for the config API."""

import unittest

from pygame_assets.exceptions import NoSuchConfigurationParameterError
from pygame_assets.configure import Config, ConfigMeta
from pygame_assets.configure import get_config, config_exists, remove_config
from pygame_assets.configure import get_environ_config, set_environ_config
from .utils import change_config, temp_config


class TestConfigMeta(unittest.TestCase):
    """Unit tests for the config._params API."""

    def test_get_class_attributes(self):
        class Foo:
            a = 1
            b = 2

            __builtins_are_ignored__ = 'bar'

            def functions_are_ignored():
                return 0

        self.assertDictEqual(ConfigMeta.get_class_attributes(Foo),
                             {'a': 1, 'b': 2})

    def test_two_config_instances_are_equal(self):
        config1 = Config()
        config2 = Config()
        self.assertEqual(config1, config2)

    def test_subconfig_inherits_config_meta(self):
        class SubConfig(Config):
            name = 'sub'

        config = Config()
        subclassed = SubConfig()
        for param in config._meta:
            self.assertIn(param, subclassed._meta)
            self.assertEqual(subclassed._meta[param], config._meta[param])

    def test_new_subconfig_parameters_are_saved(self):
        class SubConfig(Config):
            name = 'sub'

            class Meta:
                base = 'mybase'

        subclassed = SubConfig()
        self.assertEqual(subclassed._meta['base'], 'mybase')

    def test_subconfig_inherits_super_meta(self):

        with temp_config('custom', 'sub'):
            class SuperConfig(Config):
                name = 'custom'

                class Meta:
                    base = 'custom/base'

            class SubConfig(SuperConfig):
                name = 'sub'

            superconfig = SuperConfig()
            subconfig = SubConfig()
            self.assertEqual(subconfig.base, superconfig.base)

    def test_not_registered_parameter_raises_exception(self):
        with self.assertRaises(NoSuchConfigurationParameterError):
            class SubConfig(Config):
                name = 'sub'

                class Meta:
                    not_registered = 'will raise an exception'

    def test_config_has_meta_dict(self):
        config = get_config()
        self.assertIsNotNone(config._meta)
        self.assertIsInstance(config._meta, dict)

    def test_meta_contains_all_parameters(self):
        config = get_config()
        for param in ConfigMeta._allowed_params:
            self.assertIn(param, config._meta)

    def test_get_parameter_through_dot_notation(self):
        config = get_config()
        for param in config._meta:
            self.assertEqual(getattr(config, param), config._meta.get(param))

    def test_set_parameter_through_dot_notation(self):
        name = ConfigMeta._allowed_params[0]
        with change_config(name) as config:
            setattr(config, name, 'other')
            self.assertEqual('other', getattr(config, name))

    def test_set_parameter_propagates_accross_get_config(self):
        name = ConfigMeta._allowed_params[0]
        with change_config(name) as config:
            setattr(config, name, 'other')
            self.assertEqual(getattr(get_config(), name), 'other')

    def test_has_default_font_size(self):
        config = get_config()
        self.assertIsNotNone(config.default_font_size)

    def test_set_config_base(self):
        with change_config('base') as config:
            self.assertEqual('./assets', config.base)
            config.base = 'static'
            self.assertEqual('static', config.base)


class TestConfigureUtils(unittest.TestCase):
    """Test configuration management utilities."""

    def test_remove_config(self):
        class FooConfig(Config):
            name = 'foo'

        self.assertTrue(config_exists('foo'))
        remove_config('foo')
        self.assertFalse(config_exists('foo'))

    def test_config_exists(self):
        self.assertFalse(config_exists('foo'))

        class FooConfig(Config):
            name = 'foo'

        self.assertTrue(config_exists('foo'))
        remove_config('foo')


class TestConfigureFromEnv(unittest.TestCase):
    """Test the configuration from OS environment variables."""

    def setUp(self):
        set_environ_config(None)

    def test_set_environ_config(self):
        set_environ_config(None)
        self.assertIsNone(get_environ_config())
        set_environ_config('foo')
        self.assertEqual('foo', get_environ_config())

    def test_set_environ_config_to_none_is_explicit(self):
        with self.assertRaises(TypeError):
            set_environ_config()
        set_environ_config(None)

    def test_get_config_from_env_var(self):
        class MyConfig(Config):
            name = 'myconfig'

        set_environ_config('myconfig')
        config = get_config()
        self.assertEqual('myconfig', config.name)


class TestConfigDirs(unittest.TestCase):
    """Unit tests for the search directory configuration."""

    def test_config_dirs_is_dict_of_loader_names_and_dirs(self):
        config = get_config()
        for loader_name, dirs in config.dirs.items():
            self.assertIsInstance(loader_name, str)
            self.assertIsInstance(dirs, list)

    def test_search_dirs(self):
        with change_config('base', 'dirs') as config:
            config.base = 'assets'
            config.dirs['spritesheet'] = ['spritesheet', 'sheets']
            expected = ['assets/spritesheet', 'assets/sheets']
            actual = config.search_dirs('spritesheet')
            self.assertListEqual(expected, actual)


class TestConfigure(unittest.TestCase):
    """Unit tests for the Config API."""

    def setUp(self):
        set_environ_config(None)

    def test_load_default_config(self):
        explicit_config = get_config('default')
        self.assertEqual(explicit_config.name, 'default')
        no_args_config = get_config()
        self.assertEqual(no_args_config.name, 'default')

    def test_load_test_config(self):
        config = get_config('test')
        self.assertEqual(config.name, 'test')

    def test_new_config_must_have_name(self):
        with self.assertRaises(ValueError):
            class ConfigWithoutName(Config):
                name = ''

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
