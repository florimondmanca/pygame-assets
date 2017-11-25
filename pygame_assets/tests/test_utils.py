"""Tests for the testing utilities."""

import unittest
from pygame_assets import load
from pygame_assets.configure import get_environ_config, get_config, \
    Config, config_exists
from .utils import TestCase, TestConfig, change_config, temp_config, \
    define_test_text_loader


class TestTestConfig(unittest.TestCase):
    """Test the TestConfig."""

    def test_test_config(self):
        config = TestConfig()
        self.assertEqual(config.name, 'test')
        self.assertEqual(config.base, 'tests/assets')


class TestTestCase(unittest.TestCase):
    """Test the custom TestCase class."""

    def test_setup_sets_test_config(self):
        test_case = TestCase()
        self.assertEqual(get_environ_config(), None)
        test_case.setUp()
        self.assertEqual(get_environ_config(), 'test')
        self.assertEqual(get_config(), TestConfig())
        test_case.tearDown()

    def test_tear_down_cleans_up_test_config(self):
        test_case = TestCase()
        self.assertEqual(get_environ_config(), None)
        test_case.setUp()
        test_case.tearDown()
        self.assertEqual(get_environ_config(), None)


class TestDefineTestLoader(TestCase):
    """Test the define_test_text_loader context manager."""

    def test_define_test_text_loader(self):
        config = get_config()
        with define_test_text_loader() as load_text:
            self.assertIn('text', load)
            self.assertIn('text', config.dirs)
            text = load_text('test.txt')
            self.assertEqual('TEST!', text)
        self.assertNotIn('text', load)
        self.assertNotIn('text', config.dirs)


class TestChangeConfig(unittest.TestCase):
    """Test the change_config context manager."""

    def test_change_config_without_preset_config(self):
        with change_config('name') as config:
            old_value = config.name
            config.name = 'foo'
        self.assertEqual(old_value, config.name)

    def test_change_config_with_preset_config(self):
        config = get_config()
        with change_config('name', config=config):
            old_value = config.name
            config.name = 'foo'
        self.assertEqual(old_value, config.name)

    def test_change_multiple_attributes(self):
        old_values = {}
        with change_config('name', 'base') as config:
            old_values['name'] = config.name
            old_values['base'] = config.base
            config.name = 'foo'
            config.base = 'bar'
        for param in 'name base'.split():
            self.assertEqual(old_values[param], getattr(config, param))


class TestTempConfig(unittest.TestCase):
    """Test the temp_config context manager."""

    def test_temp_config(self):
        self.assertFalse(config_exists('temp'))
        with temp_config('temp'):
            class TempConfig(Config):
                name = 'temp'
            self.assertTrue(config_exists('temp'))
        self.assertFalse(config_exists('temp'))

    def test_multiple_temp_config(self):
        self.assertFalse(config_exists('temp1'))
        self.assertFalse(config_exists('temp2'))
        with temp_config('temp1', 'temp2'):
            class TempConfig1(Config):
                name = 'temp1'

            class TempConfig2(Config):
                name = 'temp2'

            self.assertTrue(config_exists('temp1'))
            self.assertTrue(config_exists('temp2'))
        self.assertFalse(config_exists('temp1'))
        self.assertFalse(config_exists('temp2'))


if __name__ == '__main__':
    unittest.main()
