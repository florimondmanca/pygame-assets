"""Tests for the loaders API."""

import unittest
import pygame

from pygame_assets.loaders import image as load_image
from pygame_assets.loaders import sound as load_sound
from pygame_assets.loaders import music as load_music
from pygame_assets.loaders import font as load_font
from pygame_assets.loaders import freetype as load_freetype
from pygame_assets.configure import get_config

from .utils import TestCase, change_config

# TODO test predefined loaders
# TODO test the custom_loaders API


class LoaderTestCase(TestCase):
    """Test case suited for loader unit testing.

    Class attributes
    ----------------
    loader : function
        A loader as defined by pygame_assets.
    filename : str
        If defined, the .asset() shortcut will be available to get the
        corresponding asset.
    """

    filename = None
    loader = None

    @classmethod
    def asset(cls, *args, **kwargs):
        if cls.filename is None:
            raise ValueError('Could not get asset: no filename defined.')
        return cls.loader(cls.filename, *args, **kwargs)


class TestImageLoader(LoaderTestCase):
    """Unit tests for the image loader."""

    loader = load_image
    filename = 'test-image.png'

    @classmethod
    def setUpClass(cls):
        pygame.init()
        # pygame requires to set_mode before loading images
        # the same constraint applies to pygame_assets
        cls.screen = pygame.display.set_mode((800, 600))

    def test_load_image_from_path(self):
        self.assertIsInstance(self.asset(), pygame.Surface)

    def test_image_with_alpha_keeps_alpha(self):
        image = load_image('test-image-with-alpha.png')
        self.assertIsNotNone(image.get_alpha())

    def test_image_without_alpha_has_no_alpha(self):
        image = load_image('test-image-without-alpha.jpg')
        self.assertIsNone(image.get_alpha())

    def test_force_convert_alpha(self):
        self.asset(convert_alpha=True)
        self.asset(convert_alpha=False)

    def test_alpha_is_kwarg_only(self):
        with self.assertRaises(TypeError):
            self.asset(True)


class TestSoundLoader(LoaderTestCase):
    """Unit tests for the sound loader."""

    loader = load_sound
    filename = 'test-sound.wav'

    def test_load_sound_from_path(self):
        self.assertIsInstance(self.asset(), pygame.mixer.Sound)

    def test_set_volume_when_loading(self):
        sound = self.asset(volume=0.5)
        self.assertEqual(sound.get_volume(), 0.5)

    def test_volume_is_kwarg_only(self):
        with self.assertRaises(TypeError):
            self.asset(0.5)


class TestMusicLoader(LoaderTestCase):
    """Unit tests for the music loader."""

    loader = load_music
    filename = 'test-sound.wav'

    def test_dir_is_sound(self):
        self.assertListEqual(get_config().dirs['music'], ['sound'])

    def test_load_music_from_path(self):
        self.assertFalse(pygame.mixer.music.get_busy())
        returned_value = self.asset()
        self.assertIsNone(returned_value)
        # music did not start playing
        self.assertFalse(pygame.mixer.music.get_busy())

    def test_set_volume_when_loading(self):
        self.asset(volume=0.5)
        self.assertEqual(pygame.mixer.music.get_volume(), 0.5)

    def test_volume_is_kwarg_only(self):
        with self.assertRaises(TypeError):
            self.asset(0.5)


class TestFontLoader(LoaderTestCase):
    """Unit tests for the font loader."""

    filename = 'bebas-neue.otf'
    loader = load_font

    @classmethod
    def setUpClass(cls):
        pygame.font.init()

    def test_load_font_from_path(self):
        self.assertIsInstance(self.asset(), pygame.font.Font)

    def test_load_with_size(self):
        self.assertAlmostEqual(self.asset(size=40).get_height(), 40, delta=10)

    def test_default_size_is_20(self):
        self.assertEqual(get_config().default_font_size, 20)
        self.assertAlmostEqual(self.asset().get_height(), 20, delta=10)

    def test_default_change_default_size(self):
        with change_config('default_font_size') as config:
            config.default_font_size = 60
            self.assertAlmostEqual(self.asset().get_height(), 60, delta=15)


class TestFreetypeFontLoader(LoaderTestCase):
    """Unit tests for the freetype font loader."""

    filename = 'bebas-neue.otf'
    loader = load_freetype

    @classmethod
    def setUpClass(cls):
        pygame.font.init()

    def test_dir_is_font(self):
        self.assertListEqual(get_config().dirs['freetype'], ['font'])

    def test_load_font_from_path(self):
        self.assertIsInstance(self.asset(), pygame.freetype.Font)

    def test_load_with_size(self):
        self.assertEqual(self.asset(size=40).size, 40)

    def test_default_size_is_20(self):
        self.assertEqual(get_config().default_font_size, 20)
        self.assertEqual(self.asset().size, 20)

    def test_default_change_default_size(self):
        with change_config('default_font_size') as config:
            config.default_font_size = 60
            self.assertEqual(self.asset().size, 60)


if __name__ == '__main__':
    unittest.main()
