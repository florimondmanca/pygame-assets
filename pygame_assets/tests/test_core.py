"""Tests for the core module."""

import unittest

from pygame_assets.core import AssetLoader, AssetLoaderMeta
from pygame_assets.exceptions import InvalidAssetLoaderNameError
from pygame_assets.configure import get_config, set_environ_config, Config


class TestConfig(unittest.TestCase):
    """Unit tests for the Config API."""

    def test_get_config_from_env_var(self):
        class MyConfig(Config):
            name = 'myconfig'

        set_environ_config('myconfig')
        config = get_config()
        self.assertEqual('myconfig', config.name)

    def test_load_default_config(self):
        set_environ_config(None)
        config = get_config()
        self.assertEqual(config.name, 'default')

    def test_load_test_config(self):
        config = get_config('test')
        self.assertEqual(config.name, 'test')

    def test_create_new_config(self):
        # verify special config does not exist already
        with self.assertRaises(KeyError):
            get_config('special')

        class SpecialConfig(Config):
            name = 'special'
            base = 'special/assets'

        # special config should now be available through get_config()
        config = get_config('special')
        self.assertEqual('special', config.name)
        self.assertEqual('special/assets', config.base)


class TestAssetLoaderMeta(unittest.TestCase):
    """Unit tests for AssetLoaderMeta, the metaclass of AssetLoader."""

    # main functional test
    def test_asset_type_of_a_dummy_loader(self):
        class DummyLoader(metaclass=AssetLoaderMeta):
            pass

        self.assertEqual('dummy', DummyLoader.asset_type)

    # detailed unit tests

    def test_get_asset_type_for_oneword_names(self):
        expected_asset_types = {
            'ImageLoader': 'image',
            'SoundLoader': 'sound',
            'FontsLoader': 'fonts',
        }
        for class_name, expected in expected_asset_types.items():
            actual = AssetLoaderMeta.get_asset_type(class_name)
            self.assertEqual(expected, actual)

    def test_get_asset_type_for_multiword_names(self):
        expected_asset_types = {
            'SoundEffectLoader': 'soundeffect',
            'SpritesheetLoader': 'spritesheet',
        }
        for class_name, expected in expected_asset_types.items():
            actual = AssetLoaderMeta.get_asset_type(class_name)
            self.assertEqual(expected, actual)

    def test_get_asset_type_without_loader_in_name(self):
        for name in ('Sounds', 'ImgLoad'):
            with self.assertRaises(InvalidAssetLoaderNameError):
                AssetLoaderMeta.get_asset_type(name)

    def test_create_asset_loader_bad_name(self):
        with self.assertRaises(InvalidAssetLoaderNameError):
            class SoundLo(metaclass=AssetLoaderMeta):
                """This should end with 'Loader'."""


class TestAssetLoader(unittest.TestCase):
    """Unit tests for the the base loader."""

    def test_meta_class_is_asset_loader_meta(self):
        self.assertEqual(type(AssetLoader), AssetLoaderMeta)

    def test_get_asset_raises_not_implemented(self):
        loader = AssetLoader()
        with self.assertRaises(NotImplementedError):
            loader.get_asset('image.png')

    def test_loader_as_function(self):
        class DummyLoader(AssetLoader):

            def get_asset(self, filepath, *tools):
                return 'Loading asset using {}'.format(', '.join(tools))

        dummy = DummyLoader.as_function()
        result = dummy('image.png', 'hammer', 'saw', 'scissors')
        self.assertEqual('Loading asset using hammer, saw, scissors',
                         result)

    def test_loader_as_function_docs_contains_asset_type(self):
        class DummyLoader(AssetLoader):
            pass

        dummy = DummyLoader.as_function()
        self.assertIn(DummyLoader.asset_type, dummy.__doc__)


if __name__ == '__main__':
    unittest.main()
