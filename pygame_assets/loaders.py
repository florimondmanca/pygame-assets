"""Generic asset management utilities for Pygame."""

import pygame
from core import AssetLoader


class SoundLoader(AssetLoader):
    """Sound asset loader."""

    def get_asset(self, file_path, *, volume=1):
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(volume)
        return sound


class ImageLoader(AssetLoader):
    """Image asset loader."""

    def get_asset(self, file_path, *, alpha=None):
        image = pygame.image.load(file_path)
        if alpha is None:
            alpha = image.get_alpha() is not None
        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image


class MusicLoader(AssetLoader):
    """Music loader."""

    def get_asset(self, file_path, *, volume=1, **kwargs):
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(**kwargs)
            pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)


class FontLoader(AssetLoader):
    """Font loader."""

    class Font(pygame.font.Font):
        """Subclass of pygame.font.Font.

        Redefines the render() function with sensible defaults.
        """

        def render(self, text, color=None, background=None, antialias=True):
            """Render the font.

            Redefinition of Pygame's font.Font.render function, only with
            sensible defaults and keyword arguments.

            Parameters
            ----------
            text : str
                The text to render.
            color : RGB tuple, optional
                Default is black (0, 0, 0).
            background : RGB tuple
                Default is None.
            antialias : bool, optional
                Default is True.
            """
            if color is None:
                color = (0, 0, 0)
            return super().render(text, antialias, color, background)

    def get_asset(self, file_path, *, size=20):
        return FontLoader.Font(file_path, size)


class FreetypeFontLoader(AssetLoader):
    """Font loader using pygame.freetype."""

    def get_asset(self, file_path, *, size=20):
        if not pygame.freetype.was_init():
            pygame.freetype.init()
        return pygame.freetype.Font(file_path, size)


sound = SoundLoader.as_function()
image = ImageLoader.as_function()
image_with_rect = ImageLoader.as_function(lambda img: (img, img.get_rect()))
music = MusicLoader.as_function()
font = FontLoader.as_function()
freetype = FreetypeFontLoader.as_function()
