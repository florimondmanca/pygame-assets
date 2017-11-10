"""Definition of custom asset loaders."""

from pygame_assets.core import AssetLoader
from pygame_assets.loaders import register


class SpritesheetLoader(AssetLoader):
    """Custom loader for spritesheets."""

    def get_asset(self, filepath):
        # dummy loader, just for the sake of example
        return 'dummy spritesheet'


# register the loader to be available in pygame_assets.load
register('spritesheet', SpritesheetLoader.as_function())
