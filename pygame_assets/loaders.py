"""Built-in function-based loaders."""

import pygame
from .core import register, loader


@loader()
def image(filepath, *, alpha=None):
    """Load an image.

    If image has alpha, calls .convert_alpha() on it.

    Note: as in regular pygame, pygame.display.set_mode() must have been
    called to load images.

    Parameters
    ----------
    filepath : str
    alpha : bool, optional
    Can be used to force alpha conversion.
    Default behavior is to detect alpha using .get_alpha().
    """
    img = pygame.image.load(filepath)
    if alpha is None:
        alpha = img.get_alpha() is not None
        if alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
    return img


@loader()
def sound(filepath, *, volume=1):
    """Load a pygame.mixer.Sound.

    Parameters
    ----------
    filepath : str
    volume : float, optional
        The volume of the sound, between 0 and 1.
        Default is 1.
    """
    sound = pygame.mixer.Sound(filepath)
    sound.set_volume(volume)
    return sound


@loader()
def music(filepath, *, volume=1, **kwargs):
    """Load a music in the pygame mixer.

    Inits the pygame mixer if needed.
    Calling pygame.mixer.play() to play the music is left to the caller.

    Parameters
    ----------
    filepath : str
    volume : float, optional
        The volume of the music, between 0 and 1.
        Default is 1.
    **kwargs : dict
        Any parameters to pass to pygame.mixer.pre_init().
    """
    if not pygame.mixer.get_init():
        pygame.mixer.pre_init(**kwargs)
        pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.set_volume(volume)


@loader()
def font(filepath, *, size=20):
    """Load a pygame.font.Font.

    Parameters
    ----------
    filepath : str
    size : int, optional
        The size of the font, in pixels.
    """
    return pygame.font.Font(filepath, size)


@loader()
def freetype(filepath, *, size=20):
    """Load a pygame.freetype.Font.

    Inits pygame.freetype if needed.

    Parameters
    ----------
    filepath : str
    size : int, optional
        The size of the font, in pixels.
    """
    if not pygame.freetype.was_init():
        pygame.freetype.init()
    return pygame.freetype.Font(filepath, size)


# register other built-in loaders

register('image_with_rect', image,
         returned=lambda img: (img, img.get_rect()))
