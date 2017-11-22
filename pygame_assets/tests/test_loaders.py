"""Tests for the loaders API."""

import unittest
import pygame

from pygame_assets.loaders import image as load_image

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


if __name__ == '__main__':
    unittest.main()
