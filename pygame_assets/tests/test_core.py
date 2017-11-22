"""Tests for the core module."""

import os
import unittest

from pygame_assets import core, load
from pygame_assets.exceptions import AssetNotFoundError
from pygame_assets.configure import get_config

from .utils import TestCase, define_test_text_loader


class TestImports(unittest.TestCase):
    """Import-related tests."""

    def test_can_import_package(self):
        import pygame_assets  # noqa: F401

    def test_package_has_version_string(self):
        import pygame_assets
        self.assertIsNotNone(pygame_assets.__version__)


class TestLoadAPI(TestCase):
    """Unit tests for the pygame_assets.load API."""

    def test_access_predefined_loaders(self):
        for loader_name in core.loaders:
            # equivalent to load.<loader_name>
            getattr(load, loader_name)

    def test_load_existing_asset(self):
        with define_test_text_loader():
            # write a test file.
            text_path = get_config().search_paths('text', 'test.txt')[0]
            with open(text_path, 'w') as textfile:
                textfile.write('TEST!')

            # load the asset using the pygame_assets.load API.
            text = load.text('test.txt')
            self.assertEqual('TEST!', text)

    def test_load_non_existing_asset_fails(self):
        with define_test_text_loader():
            with self.assertRaises(AssetNotFoundError):
                load.text('does_not_exist.txt')

    def test_get_undefined_loader_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            getattr(core.load, 'undefined!')


class TestAssetLoader(TestCase):
    """Unit tests for the the core loader functions."""

    def test_new_loader_adds_default_search_dir_to_config(self):
        config = get_config()
        self.assertNotIn('special', config.dirs)

        @core.loader()
        def special(filepath):
            pass

        self.assertIn('special', config.dirs)
        self.assertListEqual(config.dirs['special'], ['special'])

        core.unregister('special')

    def test_define_custom_name(self):
        config = get_config()
        self.assertNotIn('fantastic', config.dirs)

        @core.loader(name='fantastic')
        def special(filepath):
            pass

        self.assertIn('fantastic', config.dirs)
        # the load object has registered the loader using the custom name
        self.assertIsNotNone(load.fantastic)
        with self.assertRaises(AttributeError):
            # the function name was not used
            load.special

        core.unregister('fantastic')

    def test_custom_name_is_kwarg_only(self):
        with self.assertRaises(TypeError):
            @core.loader('should have been: name=...')
            def foo(filepath):
                pass

    def test_define_custom_search_dirs(self):
        config = get_config()
        self.assertNotIn('text', config.dirs)

        @core.loader(dirs=['levels', 'scenarios'])
        def text(filepath):
            pass

        self.assertListEqual(config.dirs['text'], ['levels', 'scenarios'])

        core.unregister('text')

    def test_load_asset(self):
        loader_name = 'text'
        get_config().add_search_dirs(loader_name, loader_name)

        filename = 'test.txt'
        content = 'TEST!'

        # define a get_asset function
        def get_text(filepath):
            with open(filepath) as textfile:
                text = textfile.read()
            return text

        # get search_paths
        search_paths = get_config().search_paths(loader_name, filename)

        # write in the test file.
        text_path = search_paths[0]
        with open(text_path, 'w') as textfile:
            textfile.write(content)

        # use the core load_asset function to load the text asset
        text = core.load_asset(get_text, filename, search_paths)
        self.assertEqual(content, text)

        # cleanup
        os.remove(text_path)
        get_config().remove_search_dirs(loader_name)


class TestRegisterApi(unittest.TestCase):
    """Unit tests for the loaders.register API."""

    def test_register_dummy_loader(self):
        with self.assertRaises(AttributeError):
            core.load.text

        def load_text(filename):
            return 'Loading {}...'.format(filename)

        # normally you'd register a real @loader() function.
        core.register('text', load_text)

        self.assertEqual(core.loaders['text'], load_text)
        self.assertEqual('Loading foo.txt...', core.load.text('foo.txt'))

        # cleanup
        core.unregister('text', in_config=False)

    def test_unregister_dummy_loader(self):

        def load_text(filename):
            return 'Loading {}...'.format(filename)

        core.register('text', load_text)
        self.assertIn('text', core.loaders)
        core.unregister('text', in_config=False)
        self.assertNotIn('text', core.loaders)

    def test_unregister_loader_removes_loader_from_config_search_dirs(self):
        @core.loader(name='text')
        def load_text(filepath):
            with open(filepath, 'r') as textfile:
                text = textfile.read()
            return text

        self.assertIn('text', get_config().dirs)
        core.unregister('text')
        self.assertNotIn('text', get_config().dirs)

    def test_register_with_returned_function(self):
        def load_text(filename):
            return 'Loading {}...'.format(filename)
        core.register('text', load_text, returned=lambda text: text.upper())
        text = load.text('foo.txt')
        self.assertEqual(text, 'LOADING FOO.TXT...')


if __name__ == '__main__':
    unittest.main()
