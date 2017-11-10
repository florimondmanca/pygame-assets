"""Custom exceptions."""


class AssetNotFoundError(ValueError):
    """Custom value error for assets not found."""

    def __init__(self, asset_filename, *args, **kwargs):
        super().__init__(asset_filename, *args, **kwargs)
