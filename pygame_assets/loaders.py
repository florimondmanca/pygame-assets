"""Generic asset management utilities for Pygame."""

import pygame
from .core import AssetLoader, AssetLoaderMeta


load_functions = {}


def register(name, load_function):
    """Allow to register custom load functions."""
    load_functions[name] = load_function


def for_asset(name):
    """Create and register a loader class from a get_asset function."""
    def create_loader(get_asset):
        def get_asset_with_self(self, filepath, *args, **kwargs):
            return get_asset(filepath, *args, **kwargs)
        cls_name = name.capitalize() + 'Loader'
        loader_cls = AssetLoaderMeta(cls_name, (AssetLoader,),
                                     {'get_asset': get_asset_with_self})
        register(name, loader_cls.as_function())
        return loader_cls

    return create_loader


class LoaderIndex:
    """When instanciated, allows to access function loaders by attribute."""

    def __getattr__(self, name):
        loader = load_functions.get(name)
        if loader is not None:
            return loader
        else:
            raise AttributeError('No such loader: {}'.format(name))


load = LoaderIndex()


# predefined loaders


@for_asset('sound')
def load_sound(self, filepath, *, volume=1):
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


@for_asset('image')
def load_image(self, filepath, *, alpha=None):
    """Load an image.

    If image has alpha, calls .convert_alpha() on it.

    Parameters
    ----------
    filepath : str
    alpha : bool, optional
        Can be used to force alpha conversion.
        Default behavior is to detect alpha using .get_alpha().
    """
    image = pygame.image.load(filepath)
    if alpha is None:
        alpha = image.get_alpha() is not None
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


@for_asset('music')
def load_music(self, filepath, *, volume=1, **kwargs):
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


@for_asset('font')
def load_font(self, filepath, *, size=20):
    """Load a pygame.font.Font.

    Parameters
    ----------
    filepath : str
    size : int, optional
        The size of the font, in pixels.
    """
    return pygame.font.Font(filepath, size)


@for_asset('freetype')
def load_freetype(self, filepath, *, size=20):
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


# register other predefined loaders

register(
    'image_with_rect',
    load_image.as_function(lambda img: (img, img.get_rect()))
)
