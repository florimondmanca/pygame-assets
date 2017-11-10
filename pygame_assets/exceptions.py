"""Custom exceptions."""


class AssetNotFoundError(ValueError):
    """Custom value error for assets not found."""

    def __init__(self, asset_filename, *args, **kwargs):
        super().__init__(asset_filename, *args, **kwargs)


class InvalidAssetLoaderNameError(ValueError):
    """Raised if a loader class has an invalid name."""

    def __init__(self, class_name, *args, **kwargs):
        message = '{} (should end with "Loader")'.format(class_name)
        super().__init__(message, *args, **kwargs)
