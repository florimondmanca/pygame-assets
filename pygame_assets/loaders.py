"""Generic asset management utilities for Pygame."""

import pygame
from .core import AssetLoader


class SoundLoader(AssetLoader):
    """Sound asset loader."""

    def get_asset(self, filepath, *, volume=1):
        sound = pygame.mixer.Sound(filepath)
        sound.set_volume(volume)
        return sound


class ImageLoader(AssetLoader):
    """Image asset loader."""

    def get_asset(self, filepath, *, alpha=None):
        image = pygame.image.load(filepath)
        if alpha is None:
            alpha = image.get_alpha() is not None
        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image


class MusicLoader(AssetLoader):
    """Music loader."""

    def get_asset(self, filepath, *, volume=1, **kwargs):
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(**kwargs)
            pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(volume)


class FontLoader(AssetLoader):
    """Font loader."""

    def get_asset(self, filepath, *, size=20):
        return pygame.font.Font(filepath, size)


class FreetypeLoader(AssetLoader):
    """Font loader using pygame.freetype."""

    def get_asset(self, filepath, *, size=20):
        if not pygame.freetype.was_init():
            pygame.freetype.init()
        return pygame.freetype.Font(filepath, size)


sound = SoundLoader.as_function()
image = ImageLoader.as_function()
image_with_rect = ImageLoader.as_function(lambda img: (img, img.get_rect()))
music = MusicLoader.as_function()
font = FontLoader.as_function()
freetype = FreetypeLoader.as_function()
