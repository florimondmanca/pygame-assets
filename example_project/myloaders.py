"""Definition of custom asset loaders."""

from pygame_assets.core import loader


@loader()
def spritesheet(filepath):
    """Dummy spritesheet loader, just for the sake of example."""
    return 'dummy spritesheet'
