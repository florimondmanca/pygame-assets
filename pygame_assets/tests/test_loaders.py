"""Tests for the loaders API."""

import unittest

from pygame_assets import loaders, load


class TestLoadApi(unittest.TestCase):
    """Unit tests for the pygame_assets.load API."""

    def test_access_predefined_loaders(self):
        for loader_name in loaders.load_functions:
            # equivalent to load.<loader_name>
            getattr(load, loader_name)


# TODO test predefined loaders
# TODO test the custom_loaders API

class TestRegisterApi(unittest.TestCase):
    """Unit tests for the loaders.register API."""

    def test_register_new_load_function(self):
        with self.assertRaises(AttributeError):
            load.text

        def load_text(filename):
            return 'Loading {}...'.format(filename)

        # normally you'd register a function from SomeLoader.as_function().
        loaders.register('text', load_text)

        self.assertEqual(loaders.load_functions['text'], load_text)
        self.assertEqual('Loading foo.txt...', load.text('foo.txt'))

        # cleanup
        del loaders.load_functions['text']

    def test_new_loader_class_using_for_asset_decorator(self):
        @loaders.for_asset('text')
        def load_text(filepath):
            return 'Loading {}...'.format(filepath)

        self.assertEqual(load_text.__name__, 'TextLoader')
        self.assertEqual('Loading tests/assets/text/foo.txt...',
                         load.text('foo.txt'))

        # cleanup
        del load_text
        del loaders.load_functions['text']


if __name__ == '__main__':
    unittest.main()
