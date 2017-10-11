import unittest
from mock import patch

from src.app import get_input_from_main_menu
from src.exception.app_exceptions import CsvFileNotSelected


class AppTests(unittest.TestCase):
    @patch('src.app.raw_input', lambda *args, **kwargs: '_')
    def test_none_numeric_input_from_main_menu_raises_value_error(self):
        self.assertRaises(ValueError, get_input_from_main_menu)
