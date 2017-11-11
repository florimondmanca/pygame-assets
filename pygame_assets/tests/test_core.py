"""Tests for the core module."""

import os
import unittest

from pygame_assets.core import AssetLoader, AssetLoaderMeta
from pygame_assets.exceptions import InvalidAssetLoaderNameError, \
    AssetNotFoundError
from pygame_assets.configure import get_config, set_environ_config, Config


class TestConfig(Config):
    """Test configuration to redefine the base assets directory."""

    name = 'test'
    base = 'tests/assets'


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
                """The name should end with 'Loader'."""


class TestAssetLoader(unittest.TestCase):
    """Unit tests for the the base loader."""

    def setUp(self):
        set_environ_config('test')

    def test_meta_class_is_asset_loader_meta(self):
        self.assertEqual(type(AssetLoader), AssetLoaderMeta)

    def test_get_asset_raises_not_implemented(self):
        loader = AssetLoader()
        with self.assertRaises(NotImplementedError):
            loader.get_asset('image.png')

    def test_new_loader_adds_default_dir_list_to_config(self):
        config = get_config()
        self.assertNotIn('special', config.dirs)

        class SpecialLoader(AssetLoader):
            pass

        self.assertIn('special', config.dirs)
        self.assertListEqual(config.dirs['special'], ['special'])

    def test_load_asset(self):
        class TextLoader(AssetLoader):

            def get_asset(self, filepath):
                with open(filepath, 'r') as textfile:
                    text = textfile.read()
                    return text

        # create a temporary test.txt file to load
        text_path = list(get_config().search_paths('text', 'test.txt'))[0]
        with open(text_path, 'w') as textfile:
            textfile.write('TEST!')

        text = TextLoader().load('test.txt')
        self.assertEqual('TEST!', text)

        # cleanup temp test.txt file
        os.remove(text_path)

    def test_load_non_existing_asset_fails(self):
        class TextLoader(AssetLoader):

            def get_asset(self, filepath):
                with open(filepath, 'r') as textfile:
                    text = textfile.read()
                return text

        with self.assertRaises(AssetNotFoundError):
            TextLoader().load('does_not_exist.txt')

    def test_loader_as_function(self):
        class ToolsImageLoader(AssetLoader):

            def get_asset(self, filepath, *tools):
                return 'Loading image using {}'.format(', '.join(tools))

        toolsimage = ToolsImageLoader.as_function()
        result = toolsimage('image.png', 'hammer', 'saw', 'scissors')
        self.assertEqual('Loading image using hammer, saw, scissors',
                         result)

    def test_loader_as_function_docs_contains_asset_type(self):
        class DummyLoader(AssetLoader):
            pass

        dummy = DummyLoader.as_function()
        self.assertIn(DummyLoader.asset_type, dummy.__doc__)


if __name__ == '__main__':
    unittest.main()
