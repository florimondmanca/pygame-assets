"""Tests for the core module."""

import unittest

from core import AssetLoader, AssetLoaderMeta


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

    def test_value_of_undefined(self):
        self.assertEqual('undefined', AssetLoaderMeta.UNDEFINED_ASSET_TYPE)

    def test_get_asset_type_without_loader(self):
        undefined = AssetLoaderMeta.UNDEFINED_ASSET_TYPE
        for name in ('Sounds', 'ImgLoad'):
            self.assertEqual(undefined, AssetLoaderMeta.get_asset_type(name))


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

            def get_asset(self, filepath, a, b, c):
                return 'Loading {} using {}'.format(filepath,
                                                    ', '.join((a, b, c)))

        dummy = DummyLoader.as_function()
        result = dummy('image.png', 'hammer', 'saw', 'scissors')
        self.assertEqual('Loading image.png using hammer, saw, scissors',
                         result)

    def test_loader_as_function_docs_contains_asset_type(self):
        class DummyLoader(AssetLoader):
            pass

        dummy = DummyLoader.as_function()
        self.assertIn(DummyLoader.asset_type, dummy.__doc__)


if __name__ == '__main__':
    unittest.main()
