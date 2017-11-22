"""Tests for the loaders API."""

import unittest
import pygame

from pygame_assets.loaders import image as load_image
from pygame_assets.loaders import sound as load_sound
from pygame_assets.loaders import music as load_music
from pygame_assets import config

# from pygame_assets import core, load
# from pygame_assets.core import register


# TODO test predefined loaders
# TODO test the custom_loaders API

class TestImageLoader(unittest.TestCase):
    """Unit tests for the image loader."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        # pygame requires to set_mode before loading images
        # the same constraint applies to pygame_assets
        cls.screen = pygame.display.set_mode((800, 600))

    def test_load_image_from_path(self):
        image = load_image('test-image.png')
        self.assertIsInstance(image, pygame.Surface)

    def test_image_with_alpha_keeps_alpha(self):
        image = load_image('test-image-with-alpha.png')
        self.assertIsNotNone(image.get_alpha())

    def test_image_without_alpha_has_no_alpha(self):
        image = load_image('test-image-without-alpha.jpg')
        self.assertIsNone(image.get_alpha())

    def test_force_convert_alpha(self):
        load_image('test-image-without-alpha.jpg', convert_alpha=True)
        load_image('test-image-with-alpha.png', convert_alpha=False)

    def test_alpha_is_kwarg_only(self):
        with self.assertRaises(TypeError):
            load_sound('test-sound.wav', True)


class TestSoundLoader(unittest.TestCase):
    """Unit tests for the sound loader."""

    def test_load_sound_from_path(self):
        sound = load_sound('test-sound.wav')
        self.assertIsInstance(sound, pygame.mixer.Sound)

    def test_set_volume_when_loading(self):
        sound = load_sound('test-sound.wav', volume=0.5)
        self.assertEqual(sound.get_volume(), 0.5)

    def test_volume_is_kwarg_only(self):
        with self.assertRaises(TypeError):
            load_sound('test-sound.wav', 0.5)


class TestMusicLoader(unittest.TestCase):
    """Unit tests for the music loader."""

    def test_dir_is_sound(self):
        self.assertListEqual(config.dirs['music'], ['sound'])

    def test_load_music_from_path(self):
        self.assertFalse(pygame.mixer.music.get_busy())
        returned_value = load_music('test-sound.wav')
        self.assertIsNone(returned_value)
        # music did not start playing
        self.assertFalse(pygame.mixer.music.get_busy())

    def test_set_volume_when_loading(self):
        load_music('test-sound.wav', volume=0.5)
        self.assertEqual(pygame.mixer.music.get_volume(), 0.5)

    def test_volume_is_kwarg_only(self):
        with self.assertRaises(TypeError):
            load_music('test-sound.wav', 0.5)


if __name__ == '__main__':
    unittest.main()
