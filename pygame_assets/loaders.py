"""Generic asset management utilities for Pygame."""

import pygame
from core import AssetLoader


class SoundLoader(AssetLoader):
    """Sound asset loader."""

    def get_asset(self, file_path, *, volume=1):
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(volume)
        return sound


def sound(filename, *, volume=1):
    """Load a sound.

    Searches for the sound in the SOUND_DIRS from the settings.py file.
    If sound is not found, raises a FileNotFound exception.

    Parameters
    ----------
    filename : str
        The sound's file name, e.g. 'click_sound.wav'.
    volume : float, optional
        The sound's volume, between 0 and 1.
        Default is 1.
    """
    return SoundLoader.load(filename, volume=volume)


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


def image(filename, *, alpha=None):
    """Load an image.

    If image is not found, raises an AssetNotFoundError.

    image('img.png') -> pygame.Surface

    Parameters
    ----------
    filename : str
        The image's file name, e.g. 'mysprite.png'.
    alpha : bool, optional
        Pass True or False to explicitly define if the image has alpha channel.
        Default is to derive it from the surface's get_alpha() value.
    """
    loader = ImageLoader()
    return loader.load(filename)


def image_with_rect(filename, *, alpha=None):
    """Load an image and return it and its rect.

    If image is not found, raises an AssetNoFoundError.

    image_with_rect('img.png') -> (pygame.Surface, pygame.Rect)

    Parameters
    ----------
    filename : str
        The image's file name, e.g. 'mysprite.png'.
    alpha : bool, optional
        Pass True or False to explicitly define if the image has alpha channel.
        Default is to derive it from the surface's get_alpha() value.
    """
    _image = image(filename, alpha=alpha)
    return _image, _image.get_rect()


class MusicLoader(AssetLoader):
    """Music loader."""

    def get_asset(self, file_path, *, volume=1, **kwargs):
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(**kwargs)
            pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)


def music(filename, *, volume=1):
    """Load a music in the pygame mixer.

    Parameters
    ----------
    filename : str
        The music's file name, e.g. 'main_theme.wav'.
    volume : float, optional
        Set the playback volume to this value
    """
    return MusicLoader.load(filename, volume=volume)


class FontLoader(AssetLoader):
    """Font loader."""

    asset_type = 'font'
    search_dirs = ''  # settings.FONT_DIRS

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


def font(filename='', *, size=20):
    """Load a font.

    Return a pygame.font.Font object.

    Parameters
    ----------
    filename : str, optional
        The font's file name, e.g. 'myfont.otf'.
        Default is settings.DEFAULT_FONT
    size : int, optional
        The font size, in pixels.
        Default is 20.
    """
    if not filename:
        filename = ''  # settings.DEFAULT_FONT
    return FontLoader.load(filename, size=size)


class FreetypeFontLoader(AssetLoader):
    """Font loader using pygame.freetype."""

    asset_type = 'font'
    search_dirs = ''  # settings.FONT_DIRS

    def get_asset(self, file_path, *, size=20):
        if not pygame.freetype.was_init():
            pygame.freetype.init()
        return pygame.freetype.Font(file_path, size)


def freetype(filename='', *, size=20):
    """Load a font.

    Return a pygame.freetype.Font object.

    Parameters
    ----------
    filename : str, optional
        The font's file name, e.g. 'myfont.otf'.
        Default is settings.DEFAULT_FONT
    size : int, optional
        The font size, in pixels.
        Default is 20.
    """
    if not filename:
        filename = ''  # settings.DEFAULT_FONT
    return FreetypeFontLoader.load(filename, size=size)
