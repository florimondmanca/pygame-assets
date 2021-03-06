"""Built-in function-based loaders."""

import pygame
import pygame.freetype
from .core import register, loader
from .configure import get_config


@loader()
def image(filepath, *, convert_alpha=None):
    """Load an image.

    Calls .convert() on the surface before returning it.
    If image has alpha, .convert_alpha() is called instead for faster blitting.
    See pygame's documentation about .convert() and .convert_alpha().

    Note: as in regular pygame, pygame.display.set_mode() must have been
    called to load images.

    Parameters
    ----------
    filepath : str
    convert_alpha : bool, optional
        Can be used to force alpha conversion.
        Default behavior is to detect alpha using .get_alpha().

    Returns
    -------
    pygame.Surface
    """
    img = pygame.image.load(filepath)

    def convert(img, alpha):
        if alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
        return img

    img = convert(
        img, img.get_alpha() if convert_alpha is None else convert_alpha)

    return img


@loader()
def sound(filepath, *, volume=1):
    """Load a sound.

    Parameters
    ----------
    filepath : str
    volume : float, optional
        The volume of the sound, between 0 and 1.
        Default is 1.

    Returns
    -------
    pygame.mixer.Sound
    """
    sound = pygame.mixer.Sound(filepath)
    sound.set_volume(volume)
    return sound


@loader(dirs=['sound'])
def music(filepath, *, volume=1, **kwargs):
    """Load a music in the pygame mixer.

    The playback will not start. Call pygame.mixer.play() to start the playback
    when desired.

    Searches in
    -----------
    sound

    Parameters
    ----------
    filepath : str
    volume : float, optional
        The volume of the music, between 0 and 1.
        Default is 1.

    Returns
    -------
    None
    """
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.set_volume(volume)


@loader()
def font(filepath, *, size=None):
    """Load a font.

    Parameters
    ----------
    filepath : str
    size : int, optional
        The size of the font, in pixels.
        Default is the config's default_font_size.

    Returns
    -------
    pygame.font.Font
    """
    if size is None:
        size = get_config().default_font_size
    return pygame.font.Font(filepath, size)


@loader(dirs=['font'])
def freetype(filepath, *, size=None):
    """Load a font using pygame.freetype.

    Inits pygame.freetype if needed.

    Searches in
    -----------
    font

    Parameters
    ----------
    filepath : str
    size : int, optional
        The size of the font, in pixels.
        Default is the config's default_font_size.

    Returns
    -------
    pygame.freetype.Font
    """
    if size is None:
        size = get_config().default_font_size
    if not pygame.freetype.was_init():
        pygame.freetype.init()
    return pygame.freetype.Font(filepath, size)


# register other built-in loaders

image_with_rect = register('image_with_rect', image,
                           returned=lambda img: (img, img.get_rect()))
