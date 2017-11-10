"""Tests for the core module."""

import unittest

from core import AssetLoader, AssetLoaderMeta


class TestAssetLoaderMeta(unittest.TestCase):
    """Unit tests for AssetLoaderMeta, the metaclass of AssetLoader."""

    def test_get_asset_type_for_oneword_names(self):
        self.assertEqual(
            'image',
            AssetLoaderMeta.get_asset_type('ImageLoader'))
        self.assertEqual(
            'sound',
            AssetLoaderMeta.get_asset_type('SoundLoader'))
        self.assertEqual(
            'fonts',
            AssetLoaderMeta.get_asset_type('FontsLoader'))

    def test_get_asset_type_for_multiword_names(self):
        self.assertEqual(
            'soundeffect',
            AssetLoaderMeta.get_asset_type('SoundEffectLoader'))
        self.assertEqual(
            'spritesheet',
            AssetLoaderMeta.get_asset_type('SpriteSheetLoader'))

    def test_value_of_undefined(self):
        self.assertEqual('undefined',
                         AssetLoaderMeta.UNDEFINED_ASSET_TYPE)

    def test_get_asset_type_without_loader(self):
        undefined = AssetLoaderMeta.UNDEFINED_ASSET_TYPE
        self.assertEqual(undefined,
                         AssetLoaderMeta.get_asset_type('Sounds'))
        self.assertEqual(undefined,
                         AssetLoaderMeta.get_asset_type('ImgLoad'))

    def test_asset_type_of_an_example_loader(self):
        class ExampleLoader(metaclass=AssetLoaderMeta):
            pass

        self.assertEqual('example', ExampleLoader.asset_type)


class TestAssetLoader(unittest.TestCase):
    """Unit tests for the the base loader."""

    def test_meta_class_is_asset_loader_meta(self):
        self.assertEqual(type(AssetLoader), AssetLoaderMeta)

    def test_get_asset_raises_not_implemented(self):
        loader = AssetLoader()
        with self.assertRaises(NotImplementedError):
            loader.get_asset('')


if __name__ == '__main__':
    unittest.main()
