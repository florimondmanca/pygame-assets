"""Custom exceptions."""


class AssetNotFoundError(ValueError):
    """Custom value error for assets not found."""

    def __init__(self, filename, search_paths, *args, **kwargs):
        message = '{} (searched in {})'.format(filename, search_paths)
        super().__init__(message, *args, **kwargs)
