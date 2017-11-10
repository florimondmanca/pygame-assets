"""Tests for custom exceptions."""

import unittest

from pygame_assets.exceptions import AssetNotFoundError
from pygame_assets.exceptions import InvalidAssetLoaderNameError


class TestExceptions(unittest.TestCase):
    """Unit tests for custom exceptions."""

    def test_asset_not_found_error_message_content(self):
        error = AssetNotFoundError('myimage.png')
        self.assertIn('myimage.png', str(error))

    def test_invalid_asset_loader_name_error_message_content(self):
        error = InvalidAssetLoaderNameError('soundloa')
        self.assertIn('soundloa', str(error))
        self.assertIn('should', str(error))
        self.assertIn('end with', str(error))
        self.assertIn('Loader', str(error))


if __name__ == '__main__':
    unittest.main()
