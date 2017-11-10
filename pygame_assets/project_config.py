"""Project configuration."""

import os


class Config:
    """Base config."""

    base = 'assets'
    dirs = {}

    def add_default_dirs(self, loader_classes):
        for loader_class in loader_classes:
            self.dirs[loader_class.asset_type] = [loader_class.asset_type]

    def search_dirs(self, asset_type):
        """Return directories where to search assets of this type.

        Returned as a generator.

        Parameters
        ----------
        asset_type : str
        """
        dirs = self.dirs.get(asset_type, [asset_type])
        return (os.path.join(self.base, dir_) for dir_ in dirs)

    def search_paths(self, asset_type, filename):
        """Return file paths where to search this asset.

        Returned as a generator.

        Parameters
        ----------
        asset_type : str
        filename : str
        """
        search_dirs = self.search_dirs(asset_type)
        return (os.path.join(dir_, filename) for dir_ in search_dirs)

    def __str__(self):
        # TODO print the config's parameters
        return super().__str__()


config = Config()
