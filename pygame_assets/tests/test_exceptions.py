"""Tests for custom exceptions."""

import unittest

from pygame_assets.exceptions import AssetNotFoundError


class TestExceptions(unittest.TestCase):
    """Unit tests for custom exceptions."""

    def test_asset_not_found_error_message_content(self):
        error = AssetNotFoundError('myimage.png', ['assets/image'])
        self.assertIn('myimage.png', str(error))
        self.assertIn('assets/image', str(error))


if __name__ == '__main__':
    unittest.main()
