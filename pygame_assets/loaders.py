"""Built-in function-based loaders."""

import pygame
from .core import register, loader


@loader()
def image(filepath, *, alpha=None):
    """Load an image.

    Calls .convert() on the surface before returning it.
    If image has alpha, .convert_alpha() is called instead for faster blitting.
    See pygame's documentation about .convert() and .convert_alpha().

    Note: as in regular pygame, pygame.display.set_mode() must have been
    called to load images.

    Parameters
    ----------
    filepath : str
    alpha : bool, optional
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

    img = convert(img, img.get_alpha() if alpha is None else alpha)

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

    Returns
    -------
    None
    """
    if not pygame.mixer.get_init():
        pygame.mixer.pre_init(**kwargs)
        pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.set_volume(volume)


@loader()
def font(filepath, *, size=20):
    """Load a font.

    Parameters
    ----------
    filepath : str
    size : int, optional
        The size of the font, in pixels.

    Returns
    -------
    pygame.font.Font
    """
    return pygame.font.Font(filepath, size)


@loader()
def freetype(filepath, *, size=20):
    """Load a font using pygame.freetype.

    Inits pygame.freetype if needed.

    Parameters
    ----------
    filepath : str
    size : int, optional
        The size of the font, in pixels.

    Returns
    -------
    pygame.freetype.Font
    """
    if not pygame.freetype.was_init():
        pygame.freetype.init()
    return pygame.freetype.Font(filepath, size)


# register other built-in loaders

register('image_with_rect', image,
         returned=lambda img: (img, img.get_rect()))
